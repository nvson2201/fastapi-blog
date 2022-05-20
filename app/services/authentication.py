from app.db import repositories
from typing import Union
from jose import jwt
from pydantic import ValidationError

from app.config import settings
from app.models.users import User
from app.exceptions.users import UserNotFound, UserInvalidCredentials


from app.db.repositories_cache.users import UserRedisRepository
from app.db.repositories.users import UserRepository
from app.utils import security
from app.schemas.tokens import TokenPayload
from app.db import repositories_cache


class AuthenticationService:

    def __init__(self,
                 crud_engine: Union[UserRedisRepository, UserRepository]):
        self.crud_engine = crud_engine

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except (jwt.JWTError, ValidationError):
            raise UserInvalidCredentials

        user = self.crud_engine.get(id=token_data.sub)

        if not user:
            raise UserNotFound

        return user


auth_services = AuthenticationService(crud_engine=repositories.users)
auth_redis_services = AuthenticationService(
    crud_engine=repositories_cache.users)
