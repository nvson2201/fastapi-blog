from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app import models
from app.api.dependencies.authentication import (
    get_current_active_user
)
from app.api.dependencies.services import get_profile_services
from app.services.exceptions.users import UserNotFound
from app.services.exceptions.profile import (
    UnableToFollowYourself, UserIsAlreadyFollowed,
    UserIsNotFollowed, UnableToUnsubcribeFromYourself
)

from app.services.profiles import ProfileServices

router = APIRouter()


@router.get("/{username}", response_model=schemas.ProfileInResponse)
def get_profile_by_username(
    username: str,
    current_user: models.User = Depends(get_current_active_user),
    profile_services: ProfileServices = Depends(get_profile_services)
) -> schemas.ProfileInResponse:
    """
    Get a specific user by id.
    """
    try:
        profile = profile_services.get_profile_by_username(
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
    current_user: models.User = Depends(get_current_active_user),
    profile_services: ProfileServices = Depends(get_profile_services)
) -> schemas.ProfileInResponse:
    try:
        profile = profile_services.follow_for_user(
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
    current_user: models.User = Depends(get_current_active_user),
    profile_services: ProfileServices = Depends(get_profile_services)
) -> schemas.ProfileInResponse:
    try:
        profile = profile_services.unsubscribe_from_user(
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
