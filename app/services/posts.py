from typing import List, Type

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.models.posts import Post
from app.schemas.posts import PostUpdate, PostCreate
from app.exceptions.posts import PostNotFound, PostDuplicate
from app.db.repositories_cache.posts import PostRedisRepository
from app.plugins.kafka import producer
from app.db import repositories_cache
from app.config import settings
from app.decorators.component import ModelType
from app.db import repositories
from app.db import db
from app.decorators.component import ComponentRepository


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

    def get(self, id: str):
        post = self.repository.get(id)
        if not post:
            raise PostNotFound

        producer.produce({'id': post.id})

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

        post = self.repository.create_with_owner(
            body=body, author_id=author_id)

        return post

    def get_multi_by_owner(
        self, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        posts = self.repository.get_multi_by_owner(
            author_id=author_id,
            skip=skip, limit=limit,
        )

        return posts

    def remove(self, id: int):
        return self.repository.remove(id)

    def update_views(self, id: int):
        self.repository.update_views(id)


post_services = PostServices(
    repository=repositories_cache.posts,
    model=Post,
    db=db,
    _crud_component=repositories.posts,
    prefix=settings.REDIS_PREFIX_USER
)
