from app.db import repositories
from typing import List, Union, Optional


from sqlalchemy import exc


from app.config import settings
from app.models.users import User
from app.schemas.users import UserUpdate, UserCreate
from app.exceptions.users import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser,
    UserInactive, UserNotSuper)
from app.utils.mail import send_new_account_email
from app.db.repositories_cache.users import UserRedisRepository
from app.db.repositories.users import UserRepository
from app.schemas.datetime import DateTime
from app.db import repositories_cache


class UserServices:

    def __init__(self,
                 crud_engine: Union[UserRedisRepository, UserRepository]):
        self.crud_engine = crud_engine

    def get_by_email(self, email: str) -> Optional[User]:
        return self.crud_engine.get_by_email(email=email)

    def get(self, id: str) -> User:
        user = self.crud_engine.get(id)

        if not user:
            raise UserNotFound

        return user

    def update(self, id: str, body: UserUpdate) -> User:
        user = self.crud_engine.get(id)

        if not user:
            raise UserNotFound

        try:
            user = self.crud_engine.update(
                user, body=body)
        except exc.IntegrityError:
            raise UserDuplicate

        return user

    def create(self, body: UserCreate) -> User:
        user = self.crud_engine.get_by_email(email=body.email)

        if user:
            raise UserDuplicate

        user = self.crud_engine.create(body=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def create_user_open(self, body: UserCreate) -> User:

        if not settings.USERS_OPEN_REGISTRATION:
            raise UserForbiddenRegiser

        user = self.crud_engine.get_by_email(email=body.email)

        if user:
            raise UserDuplicate

        user = self.crud_engine.create(body=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        return self.crud_engine.authenticate(
            email=email, password=password)

    def is_active(self, user: User) -> bool:
        if not self.crud_engine.is_active(user=user):
            raise UserInactive
        return user

    def is_superuser(self, user: User) -> bool:
        if not self.crud_engine.is_superuser(user=user):
            raise UserNotSuper
        return user

    def get_multi(
        self, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        users = self.crud_engine.get_multi(
            skip=skip, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users


user_services = UserServices(crud_engine=repositories.users)
user_redis_services = UserServices(crud_engine=repositories_cache.users)
