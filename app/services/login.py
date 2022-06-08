from typing import Any, Optional
from datetime import timedelta

from app.models.users import User

from app.services.exceptions.tokens import InvalidToken
from app.services.exceptions.users import (
    UserNotFound, UserBanned, UserIncorrectCredentials)
from app.utils.mail import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from app.utils import security
from app.utils.security import get_password_hash, verify_password
from app.config import settings
from app.schemas import UserInDB


class LoginServices:
    def __init__(self, repository, user_services):
        self.repository = repository
        self.user_services = user_services

    def authenticate(
            self, *,
            email: str,
            password: str
    ) -> Optional[User]:

        user = self.repository.get_by_email(email=email)
        if not user:
            raise UserNotFound
        if not verify_password(password, user.hashed_password):
            raise UserIncorrectCredentials
        return user

    def login_access_token(self, email: str, password: str) -> Any:
        user = self.authenticate(
            email=email,
            password=password
        )

        if not user:
            raise UserIncorrectCredentials
        elif user.is_banned:
            raise UserBanned

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

    def recover_password(self, email: str) -> Any:
        user = self.repository.get_by_email(email=email)
        if not user:
            raise UserNotFound

        password_reset_token = generate_password_reset_token(email=email)
        send_reset_password_email(
            email=email,
            email_to=user.email,
            token=password_reset_token
        )
        return {"msg": "Password recovery email sent"}

    def reset_password(
        self,
        token: str,
        new_password: str,
    ) -> Any:
        email = verify_password_reset_token(token)
        if not email:
            raise InvalidToken
        user = self.repository.get_by_email(email=email)
        if not user:
            raise UserNotFound

        hashed_password = get_password_hash(new_password)
        self.repository.update(user, body=UserInDB(
            hashed_password=hashed_password))
        return {"msg": "Password updated successfully"}
