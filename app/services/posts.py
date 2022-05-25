from typing import List, Type

from sqlalchemy import exc
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.models.posts import Post
from app.schemas.posts import (
    PostUpdate, PostCreate,
    PostInResponse, ListOfPostsInResponse,
    PostInDBCreate
)
from app.services.exceptions.posts import PostNotFound, PostDuplicate
from app.db.repositories_cache.posts import PostRedisRepository
from app.plugins.kafka import producer
from app.db import repositories_cache
from app.config import settings
from app.db.repositories_cache.decorators.component import ModelType
from app.db import repositories
from app.db import db
from app.db.repositories_cache.decorators.component import ComponentRepository
from app.models import User
from app.services.exceptions.favorites import (
    PostAlreadyFavoried, PostStillNotFavorited)


class PostServices(PostRedisRepository):

    def __init__(
        self,
        repository: PostRedisRepository,
        model: Type[ModelType],
        db: Session,
        _crud_component: ComponentRepository,
        prefix: str
    ):
        self.repository = repository
        super().__init__(model, db, _crud_component, prefix)

    def get(self, *, id: str, requested_user: User) -> PostInResponse:
        post_record = self.repository.get(id)

        if not post_record:
            raise PostNotFound

        producer.produce({'id': post_record.id})

        author = repositories.users.get_profile_by_id(
            id=post_record.author_id, requested_user=requested_user)

        tagList = self.repository.get_tags_for_post_by_id(id=post_record.id)

        favorited = self.repository.is_post_favorited_by_user(
            post=post_record, user=requested_user
        )
        favorites_count = self.repository.get_favorites_count_for_post_by_id(
            id=post_record.id)

        post = PostInResponse(
            **jsonable_encoder(post_record),
            author=author,
            tagList=tagList,
            favorited=favorited,
            favorites_count=favorites_count
        )

        return post

    def update(self, id: str, body: PostUpdate):
        post = self.repository.get(id)

        if not post:
            raise PostNotFound

        try:
            post = self.repository.update(self.post, body=body)
        except exc.IntegrityError:
            raise PostDuplicate

        return post

    def create_with_owner(self, body: PostCreate, author_id: int):
        body = jsonable_encoder(body)
        post_in_db_create = PostInDBCreate(**body, author_id=author_id)
        post_record = self.repository.create(body=post_in_db_create)

        self.repository.update_new_tags_to_post_by_id(
            id=post_record.id, tags=body['tagList'])

        author = repositories.users.get(author_id)

        post = self.get(id=post_record.id, requested_user=author)

        return post

    def get_multi_by_owner(
        self, author_id: int, offset: int = 0, limit: int = 100,
    ) -> List[Post]:

        posts = self.repository.get_multi_by_owner(
            author_id=author_id,
            offset=offset, limit=limit,
        )

        return posts

    def remove(self, id: int):
        return self.repository.remove(id)

    def update_views(self, id: int):
        self.repository.update_views(id)

    def mark_post_as_favorite(
        self, *, id: int, user: User
    ) -> PostInResponse:
        post = self.get(id=id, requested_user=user)

        if not post:
            raise PostNotFound

        if self.repository.is_post_favorited_by_user(post=post, user=user):
            raise PostAlreadyFavoried

        self.repository.add_post_into_favorites(post=post, user=user)
        post.favorites_count += 1

        return post

    def remove_post_from_favorites(
        self, *, id: int, user: User
    ) -> PostInResponse:
        post = self.get(id=id, requested_user=user)

        if not post:
            raise PostNotFound

        if not self.repository.is_post_favorited_by_user(post=post, user=user):
            raise PostStillNotFavorited

        self.repository.delete_post_from_favorites(post=post, user=user)
        post.favorites_count -= 1

        return post

    def get_posts_for_user_feed(
        self,
        *,
        user: User,
        limit: int = 20,
        offset: int = 0
    ) -> ListOfPostsInResponse:

        posts_in_db = self.repository.get_posts_for_feed(
            user=user, limit=limit, offset=offset
        )

        posts = [
            self.get(id=post.id, requested_user=user)
            for post in posts_in_db
        ]

        return ListOfPostsInResponse(
            posts=posts,
            posts_count=len(posts),
        )


post_services = PostServices(
    repository=repositories_cache.posts,
    model=Post,
    db=db,
    _crud_component=repositories.posts,
    prefix=settings.REDIS_PREFIX_USER
)
