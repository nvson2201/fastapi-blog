from typing import List
import datetime

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.schemas.user import UserUpdate, UserCreate
from app.exceptions.user import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser)
from app.utils.mail import send_new_account_email
from app.decorators.crud.redis_decorator.user import CRUDRedisUserDecorator


class UserServices:

    def __init__(self, db: Session,
                 user_redis_decorator: CRUDRedisUserDecorator):
        self.db = db
        self.user_redis_decorator = user_redis_decorator

    def get_by_id(self, id: str):
        user = self.user_redis_decorator.get(self.db, id=id)

        if not user:
            raise UserNotFound

        return user

    def update_by_id(self, id: str, body: UserUpdate):
        user = self.user_redis_decorator.get(self.db, id=id)

        if not user:
            raise UserNotFound

        try:
            user = self.user_redis_decorator.update(
                self.db, db_obj=user, obj_in=body)
        except exc.IntegrityError:
            raise UserDuplicate

        return user

    def create_user(self, body: UserCreate):
        user = self.user_redis_decorator.get_by_email(
            self.db, email=body.email)

        if user:
            raise UserDuplicate

        user = self.user_redis_decorator.create(self.db, obj_in=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def create_user_open(self, body: UserCreate):
        if not settings.USERS_OPEN_REGISTRATION:
            raise UserForbiddenRegiser

        user = self.user_redis_decorator.get_by_email(
            self.db, email=body.email)

        if user:
            raise UserDuplicate

        user = self.user_redis_decorator.create(self.db, obj_in=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def read_users(
        self, skip: int = 0, limit: int = 100,
        date_start: datetime.datetime = settings.START_TIME_DEFAULT,
        date_end: datetime.datetime = settings.LOCAL_CURRENT_TIME,
    ) -> List[User]:

        users = self.user_redis_decorator.get_multi(
            self.db, skip=skip, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users
