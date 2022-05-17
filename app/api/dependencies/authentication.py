from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import models
from app.config import settings
from app.exceptions.users import (
    UserNotFound, UserInvalidCredentials, UserInactive, UserNotSuper)
from app.services.users import UserServices
from app.api.dependencies.user_services import get_user_services

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    token: str = Depends(reusable_oauth2),
    user_services: UserServices = Depends(get_user_services)
) -> models.User:
    try:
        return user_services.get_current_user(token=token)
    except UserInvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404, detail="User not found")


def get_current_active_user(
    token: str = Depends(reusable_oauth2),
    user_services: UserServices = Depends(get_user_services)
) -> models.User:
    try:
        return user_services.get_current_active_user(token=token)
    except UserInactive:
        raise HTTPException(status_code=403, detail="Inactive user")


def get_current_active_superuser(
    token: str = Depends(reusable_oauth2),
    user_services: UserServices = Depends(get_user_services)
) -> models.User:
    try:
        return user_services.get_current_active_superuser(token=token)
    except UserNotSuper:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
