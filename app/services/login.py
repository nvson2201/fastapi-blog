from typing import Any
from datetime import timedelta

from fastapi import Depends

from app import schemas
from app.db.repositories.users import UserRepository
from app.db.repositories_cache.users import UserRedisRepository
from app.services.exceptions.tokens import InvalidToken
from app.services.exceptions.users import (
    UserNotFound,
    UserInactive,
    UserIncorrectCredentials)
from app.services.users import UserServices
from app.api.dependencies.repositories import get_redis_repo
from app.utils.mail import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from app.utils import security
from app.utils.security import get_password_hash
from app.config import settings

user_redis_repo = get_redis_repo(UserRedisRepository, UserRepository)


class LoginServices:
    user_service: UserServices
    repository: UserRedisRepository

    def __init__(
        self,
        repository: UserRedisRepository = Depends(user_redis_repo),
        user_services: UserServices = Depends()
    ):
        self.repository = repository
        self.user_services = user_services

    def login_access_token(self, email: str, password: str) -> Any:
        user = self.user_services.authenticate(
            email=email,
            password=password
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
            email=email,
            email_to=user.email,
            token=password_reset_token
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
