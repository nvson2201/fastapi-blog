from typing import Any

from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.config import settings
from app.db.repositories.posts import PostRepository


class PostRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType],
    PostRepository
):
    def __init__(self, db, _crud_component: PostRepository):
        self._crud_component = _crud_component
        RedisDecorator.__init__(self, _crud_component,
                                settings.REDIS_PREFIX_POST)
        PostRepository.__init__(self, db)

    def update_views(self, id: Any):
        post = self.crud_component.update_views(id)
        self._set_cache(id=post.id, data=post)

        return post
