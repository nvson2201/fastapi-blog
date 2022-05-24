from typing import Any, List

from app.models.posts import Post
from app.schemas.posts import PostInDBCreate
from app.db.repositories_cache.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.db import repositories
from app.config import settings
from app.db import db
from app.db.repositories.posts import PostRepository


class PostRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType],
    PostRepository
):
    def __init__(
            self, model, db,
            _crud_component: PostRepository, prefix: str):
        RedisDecorator.__init__(self, model, db, _crud_component, prefix)
        PostRepository.__init__(self, model, db)

    def create(self, *, body: PostInDBCreate) -> Post:
        post = self.crud_component.create(body=body)
        self._set_cache(id=post.id, data=post)

        return post

    def get_multi_by_owner(
        self, *, author_id: int, offset: int = 0, limit: int = 100,
    ) -> List[Post]:

        return self.crud_component.get_multi_by_owner(
            author_id=author_id, offset=offset, limit=limit,
        )

    def update_views(self, id: Any):
        post = self.crud_component.update_views(id)
        self._set_cache(id=post.id, data=post)

        return post


posts = PostRedisRepository(
    Post,
    db,
    repositories.posts,
    settings.REDIS_PREFIX_POST
)
