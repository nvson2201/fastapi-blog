from typing import List, Optional, Type

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config import settings
from app.models.users import User
from app.schemas import UserUpdate, UserCreate
from app.services.exceptions.users import (
    UserNotFound, UserDuplicate,
    UserInactive, UserNotSuper,
    UserForbiddenRegiser, UserIncorrectCredentials)
from app.utils.mail import send_new_account_email
from app.db.repositories_cache.users import UserRedisRepository
from app.schemas.datetime import DateTime
from app.db import repositories_cache
from app.decorators.component import ModelType
from app.db import repositories
from app.db import db
from app.decorators.component import ComponentRepository
from app.utils.security import verify_password


class UserServices(UserRedisRepository):

    def __init__(
        self,
        db: Session,
        prefix: str,
        model: Type[ModelType],
        repository: UserRedisRepository,
        _crud_component: ComponentRepository,
    ):
        self.repository = repository
        super().__init__(model, db, _crud_component, prefix)

    def get(self, id: str) -> User:
        user = self.repository.get(id)
        if not user:
            raise UserNotFound

        return user

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.repository.get_by_email(email=email)
        if not user:
            raise UserNotFound

        return user

    def get_by_username(self, username: str) -> Optional[User]:
        user = self.repository.get_by_username(username=username)
        if not user:
            raise UserNotFound

        return user

    def create(self, body: UserCreate) -> User:
        user = self.repository.get_by_email(email=body.email)

        if user:
            raise UserDuplicate

        user = self.repository.get_by_username(username=body.username)

        if user:
            raise UserDuplicate

        user = self.repository.create(body=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def update(self, id: str, body: UserUpdate) -> User:
        user = self.repository.get(id)

        if not user:
            raise UserNotFound

        try:
            user = self.repository.update(user, body=body)
        except exc.IntegrityError:
            raise UserDuplicate

        return user

    def create_user_open(self, body: UserCreate) -> User:

        if not settings.USERS_OPEN_REGISTRATION:
            raise UserForbiddenRegiser

        user = self.repository.get_by_email(email=body.email)

        if user:
            raise UserDuplicate

        user = self.repository.create(body=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def remove(self, *, id: int):
        user = self.repository.get(id=id)
        if not user:
            raise UserNotFound
        self.repository.remove(id=id)
        return user

    def get_multi(
        self, offset: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        users = self.repository.get_multi(
            offset=offset, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users

    def authenticate(
            self, *,
            email: str,
            password: str
    ) -> Optional[User]:

        user = self.get_by_email(email=email)
        if not user:
            raise UserNotFound
        if not verify_password(password, user.hashed_password):
            return UserIncorrectCredentials
        return user

    def is_active(self, user: User) -> bool:
        if not user.is_active:
            raise UserInactive
        return user

    def is_superuser(self, user: User) -> bool:
        if not user.is_superuser:
            raise UserNotSuper
        return user


user_services = UserServices(
    repository=repositories_cache.users,
    model=User,
    db=db,
    _crud_component=repositories.users,
    prefix=settings.REDIS_PREFIX_USER
)
