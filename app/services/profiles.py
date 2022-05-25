from typing import Optional, Type, Union

from sqlalchemy.orm import Session

from app.config import settings
from app.models.users import User
from app.schemas import Profile, ProfileInResponse
from app.services.exceptions.users import UserNotFound
from app.services.exceptions.profile import (
    UnableToFollowYourself, UserIsAlreadyFollowed,
    UserIsNotFollowed, UnableToUnsubcribeFromYourself
)

from app.db.repositories_cache.users import UserRedisRepository

from app.db import repositories_cache
from app.decorators.component import ModelType
from app.db import repositories
from app.db import db
from app.decorators.component import ComponentRepository


class ProfileServices(UserRedisRepository):

    def __init__(
        self,
        repository: UserRedisRepository,
        model: Type[ModelType],
        db: Session,
        _crud_component: ComponentRepository,
        prefix: str
    ):
        self.repository = repository
        super().__init__(model, db, _crud_component, prefix)

    def get_profile_by_id(
        self, *, id: int,
        requested_user: Optional[Union[User, Profile]]
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


profile_services = ProfileServices(
    repository=repositories_cache.users,
    model=User,
    db=db,
    _crud_component=repositories.users,
    prefix=settings.REDIS_PREFIX_USER
)
