from typing import Any, Dict, Optional, Union, List

from app.models.users import User
from app.schemas.users import UserUpdate, UserCreate
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.schemas.datetime import DateTime
from app.db import repositories
from app.config import settings


class UserRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def get_by_email(self, *, email: str) -> Optional[User]:
        user = self.crud_component.get_by_email(email=email)
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

    def get_multi(
        self, *, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        return self.crud_component.get_multi(
            skip=skip, limit=limit,
            date_start=date_start, date_end=date_end
        )

    def authenticate(self, *,
                     email: str, password: str) -> Optional[User]:
        return self.crud_component.authenticate(email=email,
                                                password=password)

    def is_active(self, user: User) -> bool:
        return self.crud_component.is_active(user=user)

    def is_superuser(self, user: User) -> bool:
        return self.crud_component.is_superuser(user=user)


users = UserRedisRepository(
    User,
    repositories.users,
    settings.REDIS_PREFIX_USER
)
