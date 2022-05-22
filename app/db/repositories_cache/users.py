from typing import Any, Dict, Optional, Union

from app.models.users import User
from app.schemas.users import UserUpdate, UserCreate
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.db.repositories.users import UserRepository
from app.db import repositories
from app.config import settings
from app.db import db


class UserRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType],
    UserRepository
):

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

    def create(self, body: UserCreate):
        user = self.crud_component.create(body=body)
        self._set_cache(id=user.id, data=user)

        return user

    def update(
        self,
        user: User,  *, body: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        user = self.crud_component.update(user=user, body=body)
        self._set_cache(id=user.id, data=user)

        return user


users = UserRedisRepository(
    User,
    db,
    repositories.users,
    settings.REDIS_PREFIX_USER
)
