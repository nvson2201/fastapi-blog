from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserUpdate, UserCreate
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator
from app.schemas.datetime import DateTime


class UserRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        user = self.crud_component.get_by_email(db, email=email)
        if user:
            self._set_cache(id=user.id, data=user)
        return user

    def get(self, db: Session, id: Any) -> Optional[User]:
        cache_data = self._get_cache(id)

        if cache_data:
            user = User(**cache_data)
        else:
            user = self.crud_component.get(db, id)
            if user:
                self._set_cache(id, data=user)

        return user

    def create(self, db: Session, body: UserCreate):
        user = self.crud_component.create(db, body=body)
        self._set_cache(id=user.id, data=user)

        return user

    def update(
        self, db: Session,
        user: User,  *, body: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        user = self.crud_component.update(db, user=user, body=body)
        self._set_cache(id=user.id, data=user)

        return user

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        return self.crud_component.get_multi(
            db, skip=skip, limit=limit,
            date_start=date_start, date_end=date_end
        )

    def authenticate(self, db: Session, *,
                     email: str, password: str) -> Optional[User]:
        return self.crud_component.authenticate(db, email=email,
                                                password=password)

    def is_active(self, user: User) -> bool:
        return self.crud_component.is_active(user=user)

    def is_superuser(self, user: User) -> bool:
        return self.crud_component.is_superuser(user=user)

    def remove(self, db: Session, id: Any):
        return self.crud_component.remove(db, id)
