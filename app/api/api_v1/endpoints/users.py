from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.services.crud_cache import UserServices
from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_user_services,
)
from app.exceptions.user import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser
)
from app.schemas.datetime import DateTime

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    date_start: DateTime = None,
    date_end: DateTime = None,
    current_user: models.User = Depends(get_current_active_superuser),
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Retrieve users by admin.
    """
    users = user_services.read_users(
        skip=skip, limit=limit,
        date_start=date_start, date_end=date_end
    )
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    body: schemas.UserCreate,
    current_user: models.User = Depends(get_current_active_superuser),
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Create new user by admin.
    """
    try:
        user = user_services.create_user(body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@router.put("/me", response_model=schemas.User)
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
        user = user_services.update_by_id(id=current_user.id, body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
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


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(get_current_active_user),
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Get a specific user by id.
    """
    try:
        user = user_services.get_by_id(id=user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    user_id: int,
    body: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_superuser),
    user_services: UserServices = Depends(get_user_services)
) -> Any:
    """
    Update a specific user by id.
    """
    try:
        user = user_services.update_by_id(id=user_id, body=body)
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
