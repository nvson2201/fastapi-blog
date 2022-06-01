from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import models
from app.config import settings
from app.services.exceptions.users import (
    UserNotFound, UserInvalidCredentials, UserInactive, UserNotSuper)
from app.services.authentication import AuthenticationService
from app.services.users import UserServices

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    token: str = Depends(reusable_oauth2),
    auth_services: AuthenticationService = Depends()
) -> models.User:
    try:
        return auth_services.get_current_user(token=token)
    except UserInvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404, detail="User not found")


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
    user_services: UserServices = Depends()
) -> models.User:
    try:
        return user_services.is_active(current_user)
    except UserInactive:
        raise HTTPException(status_code=403, detail="Inactive user")


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
    user_services: UserServices = Depends()
) -> models.User:
    try:
        return user_services.is_superuser(current_user)
    except UserNotSuper:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
