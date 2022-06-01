from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app.models.users import User
from app.schemas.tokens import TokenPayload
from app.services.exceptions.users import UserNotFound, UserInvalidCredentials
from app.db.repositories.users import UserRepository
from app.db.repositories_cache.users import UserRedisRepository
from app.api.dependencies.repositories import get_redis_repo
from app.utils import security
from app.config import settings

user_redis_repo = get_redis_repo(UserRedisRepository, UserRepository)


class AuthenticationService:
    repository: UserRedisRepository

    def __init__(
        self,
        repository: UserRedisRepository = Depends(user_redis_repo)
    ):
        self.repository = repository

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY,
                algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except (jwt.JWTError, ValidationError):
            raise UserInvalidCredentials

        user = self.repository.get(id=token_data.sub)
        if not user:
            raise UserNotFound

        return user
