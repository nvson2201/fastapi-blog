from typing import List, Union, Optional, Any
from datetime import timedelta

from sqlalchemy import exc
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError

from app.config import settings
from app.models.user import User
from app.schemas.user import UserUpdate, UserCreate
from app.exceptions.users import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser,
    UserInvalidCredentials, UserInactive, UserNotSuper,
    UserIncorrectCredentials)
from app.exceptions.tokens import InvalidToken
from app.utils.mail import send_new_account_email
from app.db.repositories_cache.users import UserRedisRepository
from app.db.repositories.users import UserRepository
from app.schemas.datetime import DateTime
from app.utils import security
from app.schemas.token import TokenPayload
from app.utils.mail import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from app.utils.security import get_password_hash
from app import schemas


class UserServices:

    def __init__(self, db: Session,
                 crud_engine: Union[UserRedisRepository, UserRepository]):
        self.db = db
        self.crud_engine = crud_engine

    def get_by_email(self, email: str) -> Optional[User]:
        return self.crud_engine.get_by_email(email=email)

    def get(self, id: str) -> User:
        user = self.crud_engine.get(self.db, id=id)

        if not user:
            raise UserNotFound

        return user

    def update(self, id: str, obj_in: UserUpdate) -> User:
        user = self.crud_engine.get(self.db, id=id)

        if not user:
            raise UserNotFound

        try:
            user = self.crud_engine.update(
                self.db, db_obj=user, obj_in=obj_in)
        except exc.IntegrityError:
            raise UserDuplicate

        return user

    def create(self, obj_in: UserCreate) -> User:
        user = self.crud_engine.get_by_email(
            self.db, email=obj_in.email)

        if user:
            raise UserDuplicate

        user = self.crud_engine.create(self.db, obj_in=obj_in)

        if settings.EMAILS_ENABLED and obj_in.email:
            send_new_account_email(
                email_to=obj_in.email,
                username=obj_in.email,
                password=obj_in.password
            )

        return user

    def create_user_open(self, obj_in: UserCreate) -> User:

        if not settings.USERS_OPEN_REGISTRATION:
            raise UserForbiddenRegiser

        user = self.crud_engine.get_by_email(
            self.db, email=obj_in.email)

        if user:
            raise UserDuplicate

        user = self.crud_engine.create(self.db, obj_in=obj_in)

        if settings.EMAILS_ENABLED and obj_in.email:
            send_new_account_email(
                email_to=obj_in.email,
                username=obj_in.email,
                password=obj_in.password
            )

        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        return self.crud_engine.authenticate(self.db,
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
            self.db, skip=skip, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except (jwt.JWTError, ValidationError):
            raise UserInvalidCredentials

        user = self.crud_engine.get(self.db, id=token_data.sub)

        if not user:
            raise UserNotFound

        return user

    def login_access_token(self, email: str, password: str) -> Any:
        """
        OAuth2 compatible token login, get an access token for future requests
        """
        user = self.authenticate(
            email=email, password=password
        )

        if not user:
            raise UserIncorrectCredentials
        elif not self.is_active(user):
            raise UserInactive

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

    def recover_password(self, email: str) -> Any:
        """
        Password Recovery
        """
        user = self.get_by_email(email=email)

        if not user:
            raise UserNotFound
        password_reset_token = generate_password_reset_token(email=email)
        send_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
        return {"msg": "Password recovery email sent"}

    def reset_password(
        self,
        token: str,
        new_password: schemas.UserPassword,
    ) -> Any:
        """
        Reset password
        """

        id = verify_password_reset_token(token)
        if not id:
            raise InvalidToken
        user = self.get(id=id)
        if not user:
            raise UserNotFound
        elif not self.is_active(user):
            raise UserInactive
        hashed_password = get_password_hash(new_password.body)
        user.hashed_password = hashed_password

        self.update(id=user.id, obj_in=user)
        return {"msg": "Password updated successfully"}
