from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.services import crud_cache
from app.api import deps
from app.utils.mail import send_new_account_email
from app.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
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
    user = crud.user.get_by_email(db, email=body.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )
    user = crud.user.create(db, obj_in=body)
    if settings.EMAILS_ENABLED and body.email:
        send_new_account_email(
            email_to=body.email,
            username=body.email,
            password=body.password
        )

    user_services._set_cache(id=user.id, data=user)

    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    body: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    try:
        user = crud.user.update(db, db_obj=current_user, obj_in=body)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
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
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=body.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )
    user = crud.user.create(db, obj_in=body)
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
    user = user_services.get_by_id(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    try:
        user = crud.user.update(db, db_obj=user, obj_in=body)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )

    user_services._set_cache(id=user.id, data=user)

    return user
