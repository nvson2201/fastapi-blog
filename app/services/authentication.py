from jose import jwt
from pydantic import ValidationError

from app.models.users import User
from app.schemas.tokens import TokenPayload
from app.services.exceptions.users import UserNotFound, UserInvalidCredentials
from app.utils import security
from app.config import settings


class AuthenticationService:
    def __init__(self, repository):
        self.repository = repository

    def get_current_user(self, token: str) -> User:
        try:
            print(token)
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
