from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app import models
from app.api.dependencies.authentication import (
    get_current_active_user
)
from app.exceptions.users import UserNotFound
from app.exceptions.profile import (
    UnableToFollowYourself, UserIsAlreadyFollowed,
    UserIsNotFollowed, UnableToUnsubcribeFromYourself)

from app.services.users import user_services

router = APIRouter()


@router.get("/{username}", response_model=schemas.ProfileInResponse)
def get_profile_by_username(
    username: str,
    current_user: models.User = Depends(get_current_active_user)
) -> schemas.ProfileInResponse:
    """
    Get a specific user by id.
    """
    try:
        profile = user_services.get_profile_by_username(
            username=username,
            requested_user=current_user
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return schemas.ProfileInResponse(profile=profile)


@router.post("/{username}", response_model=schemas.ProfileInResponse)
def follow_for_user(
    username: str,
    current_user: models.User = Depends(get_current_active_user)
) -> schemas.ProfileInResponse:
    try:
        profile = user_services.follow_for_user(
            username=username, requested_user=current_user)

    except UnableToFollowYourself:
        raise HTTPException(
            status_code=400,
            detail='Unable to follow yourself!'
        )

    except UserIsAlreadyFollowed:
        raise HTTPException(
            status_code=400,
            detail='User is already followed!'
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return profile


@router.delete("/{username}", response_model=schemas.ProfileInResponse)
def unsubscribe_from_user(
    username: str,
    current_user: models.User = Depends(get_current_active_user)
) -> schemas.ProfileInResponse:
    try:
        profile = user_services.unsubscribe_from_user(
            username=username, requested_user=current_user)
    except UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    except UnableToUnsubcribeFromYourself:
        raise HTTPException(
            status_code=400,
            detail='Unable to unsubcribe from yourself!',
        )
    except UserIsNotFollowed:
        raise HTTPException(
            status_code=400,
            detail='User is not followed!'
        )

    return profile
