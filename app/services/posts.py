from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc

from app.schemas.posts import (
    PostUpdate, PostCreate,
    PostInResponse, ListOfPostsInResponse,
    PostInDBCreate
)
from app.models import User
from app.plugins.kafka import producer
from app.services.exceptions.favorites import (
    PostAlreadyFavoried, PostStillNotFavorited)
from app.services.exceptions.posts import PostNotFound, PostDuplicate


class PostServices:
    def __init__(self, repository, profile_services):
        self.repository = repository
        self.profile_services = profile_services

    def get(self, *, id: str, requested_user: User) -> PostInResponse:
        post_record = self.repository.get(id)

        if not post_record:
            raise PostNotFound

        producer.produce(
            {'id': post_record.id}
        )

        author = self.profile_services.get_profile_by_id(
            id=post_record.author_id,
            requested_user=requested_user
        )
        tagList = self.repository.get_tags_for_post_by_id(
            id=post_record.id
        )
        favorited = self.repository.is_post_favorited_by_user(
            post=post_record,
            user=requested_user
        )
        favorites_count = self.repository.get_favorites_count_for_post_by_id(
            id=post_record.id
        )

        post = PostInResponse(
            **jsonable_encoder(post_record),
            author=author,
            tagList=tagList,
            favorited=favorited,
            favorites_count=favorites_count
        )

        return post

    def update(self, *, id: str, body: PostUpdate, requested_user: User):

        post_in_db = self.repository.get(id)

        if not post_in_db:
            raise PostNotFound
        try:
            self.repository.update(post_in_db, body=body)
        except exc.IntegrityError:
            raise PostDuplicate

        old_tags = list(
            set(self.repository.get_tags_for_post_by_id(id=id)) -
            set(body.tags)
        )

        new_tags = list(set(body.tags) - set(old_tags))

        self.remove_link_tags_to_post_by_id(
            id=id, tags=old_tags
        )
        self.link_new_tags_to_post_by_id(
            id=id, tags=new_tags
        )

        post_in_response = self.get(
            id=id, requested_user=requested_user
        )

        return post_in_response

    def create_with_owner(self, body: PostCreate, author_id: int):

        body = jsonable_encoder(body)

        post_in_db_create = PostInDBCreate(
            **body, author_id=author_id
        )

        post_record = self.repository.create(
            body=post_in_db_create
        )

        notification_message = {
            "content": "Created new post!",
            "sender_id": author_id,
            "post_id": post_record.id
        }

        producer.produce(
            notification_message
        )

        self.repository.link_new_tags_to_post_by_id(
            id=post_record.id, tags=body['tagList']
        )

        author = self.profile_services.get_profile_by_id(id=author_id)

        post = self.get(
            id=post_record.id,
            requested_user=author
        )

        return post

    def posts_filters(
        self,
        *,
        tags: Optional[str] = None,
        author: Optional[str] = None,
        user_favorited: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        requested_user: Optional[User] = None,
    ) -> ListOfPostsInResponse:

        tags = tags.split(",")
        tags = [tag.strip() for tag in tags]

        posts_in_db = self.repository.posts_filters(
            tags=tags,
            author=author,
            user_favorited=user_favorited,
            limit=limit,
            offset=offset,
            requested_user=requested_user
        )
        posts = [
            self.get(
                id=post.id,
                requested_user=requested_user
            )
            for post in posts_in_db
        ]

        return ListOfPostsInResponse(
            posts=posts,
            posts_count=len(posts),
        )

    def remove(self, *, id: int, requested_user: User):

        post = self.get(
            id=id,
            requested_user=requested_user
        )
        self.repository.remove(id=id)
        return post

    def update_views(self, id: int):
        self.repository.update_views(id)

    def mark_post_as_favorite(
        self, *, id: int, user: User
    ) -> PostInResponse:
        post = self.get(
            id=id,
            requested_user=user
        )

        if not post:
            raise PostNotFound

        if self.repository.is_post_favorited_by_user(
                post=post,
                user=user
        ):
            raise PostAlreadyFavoried

        self.repository.add_post_into_favorites(
            post=post, user=user
        )

        post.favorites_count += 1

        return post

    def remove_post_from_favorites(
        self, *, id: int, user: User
    ) -> PostInResponse:
        post = self.get(id=id, requested_user=user)

        if not post:
            raise PostNotFound

        if not self.repository.is_post_favorited_by_user(
                post=post, user=user
        ):
            raise PostStillNotFavorited

        self.repository.delete_post_from_favorites(
            post=post, user=user
        )

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
            user=user,
            limit=limit,
            offset=offset
        )

        posts = [
            self.get(
                id=post.id,
                requested_user=user
            )
            for post in posts_in_db
        ]

        return ListOfPostsInResponse(
            posts=posts,
            posts_count=len(posts),
        )
