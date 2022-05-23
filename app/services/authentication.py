from jose import jwt
from pydantic import ValidationError

from app.config import settings
from app.models.users import User
from app.services.exceptions.users import UserNotFound, UserInvalidCredentials

from app.db.repositories_cache.users import UserRedisRepository
from app.utils import security
from app.schemas.tokens import TokenPayload
from app.db import repositories_cache


class AuthenticationService:

    def __init__(self, repository: UserRedisRepository):
        self.repository = repository

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except (jwt.JWTError, ValidationError):
            raise UserInvalidCredentials

        user = self.repository.get(id=token_data.sub)

        if not user:
            raise UserNotFound

        return user


auth_services = AuthenticationService(repository=repositories_cache.users)
