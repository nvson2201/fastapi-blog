from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.services import crud_cache
from app.api import deps
from app.services.crud_cache.exceptions import (
    UserNotFound, UserDuplicate, UserForbiddenRegiser
)

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    user_services: crud_cache.UserServices = Depends(deps.get_user_services)
) -> Any:
    """
    Retrieve users.
    """
    users = user_services.read_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    body: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    user_services: crud_cache.UserServices = Depends(deps.get_user_services)
) -> Any:
    """
    Create new user.
    """
    try:
        user = user_services.create_user(db, body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    body: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    user_services: crud_cache.UserServices = Depends(deps.get_user_services)
) -> Any:
    """
    Update own user.
    """
    try:
        user = user_services.update_by_id(db, id=current_user.id, body=body)
    except UserDuplicate:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    body: schemas.UserCreate,
    user_services: crud_cache.UserServices = Depends(deps.get_user_services)
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    try:
        user = user_services.create_user(db, body=body)
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
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
    user_services: crud_cache.UserServices = Depends(deps.get_user_services)
) -> Any:
    """
    Get a specific user by id.
    """
    try:
        user = user_services.get_by_id(db, id=user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    body: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    user_services: crud_cache.UserServices = Depends(deps.get_user_services)
) -> Any:
    """
    Update a user.
    """
    try:
        user = user_services.update_by_id(db, id=user_id, body=body)
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
