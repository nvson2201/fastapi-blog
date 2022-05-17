from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from app import models, schemas
from app.api.dependencies import authentication
from app.exceptions.tokens import InvalidToken
from app.exceptions.users import (
    UserNotFound, UserInactive, UserIncorrectCredentials)
from app.api.dependencies.user_services import get_user_services
from app.services.users import UserServices

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        token = user_services.login_access_token(
            email=form_data.username, password=form_data.password
        )
    except UserIncorrectCredentials:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    except UserInactive:
        raise HTTPException(
            status_code=403,
            detail="Inactives user"
        )
    return token


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User
               = Depends(authentication.get_current_active_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(
    email: str,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Password Recovery
    """

    try:
        user_services.recover_password(email=email)
    except UserNotFound:
        HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str,
    new_password: schemas.UserPassword,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Reset password
    """
    try:
        user_services.recover_password(token=token, new_password=new_password)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid token")
    except UserNotFound:
        HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    except UserInactive:
        raise HTTPException(status_code=403, detail="Inactive user")

    return {"msg": "Password updated successfully"}
