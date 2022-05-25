from typing import Optional

from app.models.users import User
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.db.repositories.users import UserRepository
from app.config import settings


class UserRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType],
    UserRepository
):
    def __init__(self, db, _crud_component: UserRepository):
        RedisDecorator.__init__(self, _crud_component,
                                settings.REDIS_PREFIX_USER)
        UserRepository.__init__(self, db)

    def get_by_email(self, *, email: str) -> Optional[User]:
        user = self.crud_component.get_by_email(email=email)
        if user:
            self._set_cache(id=user.id, data=user)

        return user

    def get_by_username(self, *, username: str) -> Optional[User]:
        user = self.crud_component.get_by_username(username=username)
        if user:
            self._set_cache(id=user.id, data=user)

        return user
