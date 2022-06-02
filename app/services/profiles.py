from typing import Optional, Union

from app.models.users import User
from app.schemas import Profile, ProfileInResponse
from app.services.exceptions.users import UserNotFound
from app.services.exceptions.profile import (
    UnableToFollowYourself, UserIsAlreadyFollowed,
    UserIsNotFollowed, UnableToUnsubcribeFromYourself
)


class ProfileServices:

    def __init__(self, repository):
        self.repository = repository

    def get_profile_by_id(
        self, *, id: int,
        requested_user: Optional[Union[User, Profile]] = None,
    ) -> Optional[Union[User, Profile]]:

        user = self.repository.get(id)

        if not user:
            raise UserNotFound

        profile = Profile(**user.__dict__)

        if requested_user:
            profile.following = self.repository.is_user_following_for_another(
                target_user=user,
                requested_user=requested_user,
            )
        return profile

    def get_profile_by_username(
        self, *, username: str,
        requested_user: Optional[Union[User, Profile]]
    ) -> Optional[Union[User, Profile]]:

        user = self.repository.get_by_username(username=username)

        if not user:
            raise UserNotFound

        profile = Profile(**user.__dict__)

        if requested_user:
            profile.following = self.repository.is_user_following_for_another(
                target_user=user,
                requested_user=requested_user,
            )
        return profile

    def follow_for_user(
        self,
        *,
        username: str,
        requested_user: Optional[Union[User, Profile]]
    ) -> None:

        profile = self.get_profile_by_username(
            username=username,
            requested_user=requested_user
        )

        if requested_user.username == profile.username:
            raise UnableToFollowYourself
        if profile.following:
            raise UserIsAlreadyFollowed

        self.repository.add_user_into_followers(
            target_user=profile,
            requested_user=requested_user
        )

        return ProfileInResponse(profile=profile.copy(
            update={"following": True})
        )

    def unsubscribe_from_user(
        self,
        *,
        username: str,
        requested_user: Optional[Union[User, Profile]]
    ) -> None:
        profile = self.get_profile_by_username(
            username=username,
            requested_user=requested_user
        )

        if requested_user.username == profile.username:
            raise UnableToUnsubcribeFromYourself

        if not profile.following:
            raise UserIsNotFollowed

        self.repository.remove_user_from_followers(
            target_user=profile,
            requested_user=requested_user
        )

        return ProfileInResponse(profile=profile.copy(
            update={"following": False})
        )
