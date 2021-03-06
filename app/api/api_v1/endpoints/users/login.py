from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas
from app.api.dependencies import authentication
from app.api.dependencies.services import get_login_services
from app.services.exceptions.tokens import InvalidToken
from app.services.exceptions.users import (
    UserInactive, UserIncorrectCredentials, UserNotFound,
)
from app.services.login import LoginServices

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_services: LoginServices = Depends(get_login_services)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        token = login_services.login_access_token(
            email=form_data.username, password=form_data.password
        )
    except UserIncorrectCredentials:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    except UserNotFound:
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


@router.post("/login/test-token", response_model=schemas.UserInResponse)
def test_token(current_user: models.User
               = Depends(authentication.get_current_active_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/logout", response_model=schemas.UserInResponse)
def test_token2(current_user: models.User
                = Depends(authentication.get_current_active_user)) -> Any:
    """
    Logout user
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(
    email: str,
    login_services: LoginServices = Depends(get_login_services)
) -> Any:
    """
    Password Recovery
    """

    try:
        login_services.recover_password(email=email)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    return {"msg": "Password recovery email sent"}


@router.post("/reset-password", response_model=schemas.Msg)
def reset_password(
    reset_password: schemas.ResetPassword,
    login_services: LoginServices = Depends(get_login_services),
) -> Any:
    """
    Reset password
    """
    try:
        login_services.reset_password(
            token=reset_password.token, new_password=reset_password.body)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid token")
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    except UserInactive:
        raise HTTPException(status_code=403, detail="Inactive user")

    return {"msg": "Password updated successfully"}
