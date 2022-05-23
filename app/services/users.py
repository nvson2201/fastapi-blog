from typing import List, Optional, Type, Union

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.config import settings
from app.models.users import User
from app.schemas import UserUpdate, UserCreate, Profile, ProfileInResponse
from app.exceptions.users import (
    UserNotFound, UserDuplicate,
    UserInactive, UserNotSuper, UserForbiddenRegiser)
from app.exceptions.profile import (
    UnableToFollowYourself, UserIsAlreadyFollowed,
    UserIsNotFollowed, UnableToUnsubcribeFromYourself
)

from app.utils.mail import send_new_account_email
from app.db.repositories_cache.users import UserRedisRepository
from app.schemas.datetime import DateTime
from app.db import repositories_cache
from app.decorators.component import ModelType
from app.db import repositories
from app.db import db
from app.decorators.component import ComponentRepository


class UserServices(UserRedisRepository):

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

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.repository.get_by_email(email=email)
        if not user:
            raise UserNotFound

        return user

    def get_by_username(self, username: str) -> Optional[User]:
        user = self.repository.get_by_username(username=username)
        if not user:
            raise UserNotFound

        return user

    def get(self, id: str) -> User:
        user = self.repository.get(id)
        if not user:
            raise UserNotFound

        return user

    def update(self, id: str, body: UserUpdate) -> User:
        user = self.repository.get(id)

        if not user:
            raise UserNotFound

        try:
            user = self.repository.update(user, body=body)
        except exc.IntegrityError:
            raise UserDuplicate

        return user

    def create(self, body: UserCreate) -> User:
        user = self.repository.get_by_email(email=body.email)

        if user:
            raise UserDuplicate

        user = self.repository.get_by_username(username=body.username)

        if user:
            raise UserDuplicate

        user = self.repository.create(body=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def create_user_open(self, body: UserCreate) -> User:

        if not settings.USERS_OPEN_REGISTRATION:
            raise UserForbiddenRegiser

        user = self.repository.get_by_email(email=body.email)

        if user:
            raise UserDuplicate

        user = self.repository.create(body=body)

        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        return self.repository.authenticate(
            email=email, password=password)

    def is_active(self, user: User) -> bool:
        if not self.repository.is_active(user=user):
            raise UserInactive
        return user

    def is_superuser(self, user: User) -> bool:
        if not self.repository.is_superuser(user=user):
            raise UserNotSuper
        return user

    def get_multi(
        self, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        users = self.repository.get_multi(
            skip=skip, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users

    def get_profile_by_username(
        self, *, username: str,
        requested_user: Optional[Union[User, Profile]]
    ) -> Optional[Union[User, Profile]]:

        profile = self.repository.get_profile_by_username(
            username=username, requested_user=requested_user)

        if not profile:
            raise UserNotFound

        return profile

    def follow_for_user(
        self,
        *,
        username: str,
        requested_user: Optional[Union[User, Profile]]
    ) -> None:

        profile = self.get_profile_by_username(
            username=username, requested_user=requested_user)

        if requested_user.username == profile.username:
            raise UnableToFollowYourself
        if profile.following:
            raise UserIsAlreadyFollowed

        self.repository.add_user_into_followers(
            target_user=profile, requested_user=requested_user
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
            username=username, requested_user=requested_user)

        if requested_user.username == profile.username:
            raise UnableToUnsubcribeFromYourself

        if not profile.following:
            raise UserIsNotFollowed

        self.repository.remove_user_from_followers(
            target_user=profile, requested_user=requested_user
        )

        return ProfileInResponse(profile=profile.copy(
            update={"following": False})
        )


user_services = UserServices(
    repository=repositories_cache.users,
    model=User,
    db=db,
    _crud_component=repositories.users,
    prefix=settings.REDIS_PREFIX_USER
)
