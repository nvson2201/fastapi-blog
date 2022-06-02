from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.api.dependencies.authentication import (
    get_current_active_superuser,
    get_current_active_user,
)
from app.api.dependencies.services import get_user_services
from app.services.exceptions.users import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser
)
from app.schemas.datetime import DateTime
from app.services.users import UserServices

router = APIRouter()


@ router.get(
    "/",
    response_model=List[schemas.UserInResponse],
    dependencies=[Depends(get_current_active_superuser)]
)
def read_users(
    offset: int = 0,
    limit: int = 100,
    date_start: DateTime = None,
    date_end: DateTime = None,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Retrieve users by admin.
    """
    users = user_services.get_multi(
        offset=offset, limit=limit,
        date_start=date_start, date_end=date_end
    )
    return users


@router.post(
    "/",
    response_model=schemas.UserInResponse,
    dependencies=[Depends(get_current_active_superuser)]
)
def create_user(
    *,
    body: schemas.UserCreate,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Create new user by admin.
    """
    try:
        user = user_services.create(body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@ router.put("/me", response_model=schemas.UserInResponse)
def update_user_me(
    *,
    body: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_user),
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Update own user.
    """
    try:
        user = user_services.update(id=current_user.id, body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@ router.get("/me", response_model=schemas.UserInResponse)
def read_user_me(
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@ router.post("/open", response_model=schemas.UserInResponse)
def create_user_open(
    *,
    body: schemas.UserCreate,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    try:
        user = user_services.create_user_open(body=body)
    except UserForbiddenRegiser:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@ router.get(
    "/{user_id}",
    response_model=schemas.UserInResponse,
    dependencies=[Depends(get_current_active_user)]
)
def read_user_by_id(
    user_id: int,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Get a specific user by id.
    """
    try:
        user = user_services.get(id=user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@ router.put(
    "/{user_id}",
    response_model=schemas.UserInResponse,
    dependencies=[Depends(get_current_active_superuser)]
)
def update_user(
    *,
    user_id: int,
    body: schemas.UserUpdate,
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Update a specific user by id.
    """
    try:
        user = user_services.update(id=user_id, body=body)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user
