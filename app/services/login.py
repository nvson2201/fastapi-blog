from typing import Any
from datetime import timedelta

from app import schemas
from app.config import settings

from app.exceptions.users import (
    UserNotFound,
    UserInactive,
    UserIncorrectCredentials)
from app.exceptions.tokens import InvalidToken
from app.db.repositories_cache.users import UserRedisRepository
from app.utils import security
from app.utils.mail import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from app.utils.security import get_password_hash
from app.db import repositories_cache


class LoginServices:

    def __init__(self, repository: UserRedisRepository):
        self.repository = repository

    def login_access_token(self, email: str, password: str) -> Any:
        user = self.repository.authenticate(
            email=email, password=password
        )

        if not user:
            raise UserIncorrectCredentials
        elif not self.repository.is_active(user):
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
        user = self.repository.get_by_email(email=email)

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
        id = verify_password_reset_token(token)
        if not id:
            raise InvalidToken
        user = self.repository.get(id)
        if not user:
            raise UserNotFound
        elif not self.repository.is_active(user):
            raise UserInactive
        hashed_password = get_password_hash(new_password.body)
        user.hashed_password = hashed_password

        self.repository.update(id=user.id, body=user)
        return {"msg": "Password updated successfully"}


login_services = LoginServices(repository=repositories_cache.users)
