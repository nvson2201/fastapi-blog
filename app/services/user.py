from typing import List, Union

from sqlalchemy import exc
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError

from app.config import settings
from app.models.user import User
from app.schemas.user import UserUpdate, UserCreate
from app.exceptions.user import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser,
    UserInvalidCredentials, UserInactive, UserNotSuper)
from app.utils.mail import send_new_account_email
from app.db.repositories_cache.user import CRUDRedisUserDecorator
from app.db.repositories.crud_user import CRUDUser
from app.schemas.datetime import DateTime
from app.utils import security
from app import schemas


class UserServices:

    def __init__(self, db: Session,
                 crud_engine: Union[CRUDRedisUserDecorator, CRUDUser]):
        self.db = db
        self.crud_engine = crud_engine

    def get_by_id(self, id: str):
        user = self.crud_engine.get(self.db, id=id)

        if not user:
            raise UserNotFound

        return user

    def update_by_id(self, id: str, body: UserUpdate):
        user = self.crud_engine.get(self.db, id=id)

        if not user:
            raise UserNotFound

        try:
            user = self.crud_engine.update(
                self.db, db_obj=user, obj_in=body)
        except exc.IntegrityError:
            raise UserDuplicate

        return user

    def create_user(self, body: UserCreate):
        user = self.crud_engine.get_by_email(
            self.db, email=body.email)

        if user:
            raise UserDuplicate

        user = self.crud_engine.create(self.db, obj_in=body)

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

        user = self.crud_engine.get_by_email(
            self.db, email=body.email)

        if user:
            raise UserDuplicate

        user = self.crud_engine.create(self.db, obj_in=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def read_users(
        self, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        users = self.crud_engine.get_multi(
            self.db, skip=skip, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users

    def get_current_user(self, token: str):

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = schemas.TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            raise UserInvalidCredentials

        user = self.crud_engine.get(self.db, id=token_data.sub)

        if not user:
            raise UserNotFound

        return user

    def get_current_active_user(self, token: str):
        user = self.get_current_user(token=token)

        if not self.crud_engine.is_active(user):
            raise UserInactive

        return user

    def get_current_active_superuser(self, token: str):
        user = self.get_current_user(token=token)

        if not self.crud_engine.is_superuser(user):
            raise UserNotSuper

        return user
