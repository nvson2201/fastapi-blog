from typing import Any, List

from app.models.posts import Post
from app.schemas.posts import PostCreate
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.db import repositories
from app.config import settings


class PostRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def create_with_owner(self,
                          body: PostCreate, author_id: int):
        post = self.crud_component.create_with_owner(
            body=body, author_id=author_id)

        self._set_cache(id=post.id, data=post)

        return post

    def get_multi_by_owner(
        self, *, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        return self.crud_component.get_multi_by_owner(
            author_id=author_id, skip=skip, limit=limit,
        )

    def update_views(self, id: Any):
        post = self.crud_component.update_views(id)
        self._set_cache(id=post.id, data=post)
        return post


posts = PostRedisRepository(
    Post,
    repositories.posts,
    settings.REDIS_PREFIX_POST
)
