from app.decorators.crud.redis_decorator.user import CRUDRedisUserDecorator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.utils import security
from app.config import settings
from app.services.crud_cache import UserServices
from app.api.dependencies.database import get_db


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> models.User:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

    user = crud.user.get(db, id=token_data.sub)

    if not user:
        raise HTTPException(
            status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


crud_engine = CRUDRedisUserDecorator(
    crud.user, settings.REDIS_SUFFIX_USER
)


def get_user_services(
    db: Session = Depends(get_db)
):
    return UserServices(db, crud_engine=crud_engine)
