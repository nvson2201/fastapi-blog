from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException

from app import schemas
from app.api.dependencies.services import get_register_services
from app.services.exceptions.users import (
    InvalidCode, UserLimitSendCode, UserNotFound, UserDuplicate,
    UserNeedToWaitForNextVerify
)
from app.services.register import RegisterServices

router = APIRouter()


@router.post("/register", response_model=schemas.UserInResponse)
def register(
    *,
    body: schemas.UserCreate,
    register_services: RegisterServices = Depends(get_register_services)
) -> Any:
    """
    Register User
    """
    try:
        user = register_services.register(body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@router.post(
    "/send_code"
)
def send_code(
    *,
    user_id: int = Body(default=None, embed=True, gt=1),
    register_services: RegisterServices = Depends(get_register_services)
) -> Any:
    try:
        register_services.send_code(user_id=user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    except UserLimitSendCode:
        raise HTTPException(
            status_code=403,
            detail="You need to wait 1 minutes for next send",
        )

    return {"msg": "Code successfully sent, please check your email"}


@ router.post(
    "/verify-new-account"
)
def verify_new_account(
    *,
    user_id: int = Body(...),
    code_str: str = Body(...),
    register_services: RegisterServices = Depends(get_register_services)
) -> Any:
    try:
        register_services.verify_code_for_registers(
            user_id=user_id, code_str=code_str)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    except UserNeedToWaitForNextVerify:
        raise HTTPException(
            status_code=403,
            detail="You exceed 5 times failed to verify, plase wait 1 hours!",
        )
    except InvalidCode:
        raise HTTPException(
            status_code=401,
            detail="Your code is incorrect!",
        )

    return {"msg": "Register successfully!"}
