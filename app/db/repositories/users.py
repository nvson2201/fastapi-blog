from typing import List
from typing import Any, Dict, Optional, Union

from app.schemas.users import UserCreate, UserUpdate, UserInDB
from app.schemas.profiles import Profile
from app.schemas.datetime import DateTime
from app.models.users import User
from app.models.followers_to_followings import FollowersToFollowings
from app.services.exceptions.profile import UserIsNotFollowed
from app.db.repositories.base import BaseRepository
from app.utils.security import get_password_hash
from app.config import settings


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):

    def __init__(self, db):
        super().__init__(User, db)

    def get_by_email(self, *, email: str) -> Optional[User]:
        q = self.db.query(User)
        q = q.filter(User.email == email)
        user = q.first()

        return user

    def get_by_username(self, *, username: str) -> Optional[User]:
        q = self.db.query(User)
        q = q.filter(User.username == username)
        user = q.first()

        return user

    def create(self, *, body: Union[UserCreate, Dict[str, Any]]) -> User:

        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        hashed_password = get_password_hash(body_dict['password'])
        created_at = settings.current_time()

        create_data = UserInDB(
            hashed_password=hashed_password,
            created_at=created_at,
            updated_at=created_at,
            **body_dict
        )

        return super().create(body=create_data)

    def update(
        self,
        user: User, *, body: Union[UserUpdate, Dict[str, Any]]
    ) -> User:

        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        if 'password' in body_dict:
            hashed_password = get_password_hash(body_dict['password'])
            body_dict['hashed_password'] = hashed_password
            del body_dict['password']

        updated_at = settings.current_time()

        update_data = UserInDB(
            updated_at=updated_at,
            **body_dict
        )

        return super().update(user, body=update_data)

    def get_multi(
        self, *, offset: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        q = self.db.query(User)

        if date_start is None:
            date_start = DateTime(datetime=settings.past_week())
        q = q.filter(User.created_at >= date_start.datetime)

        if date_end is None:
            date_end = DateTime(datetime=settings.current_time())

        q = q.filter(User.created_at <= date_end.datetime)
        q = q.limit(limit)
        q = q.offset(offset)

        users = q.all()

        return users

    def is_user_following_for_another(
        self,
        *,
        target_user: Optional[Union[User, Profile]],
        requested_user: Optional[Union[User, Profile]]
    ) -> bool:

        q = self.db.query(FollowersToFollowings)

        q = q.filter(
            FollowersToFollowings.following_id == target_user.id
        )

        followers_to_followings_record = q.filter(
            FollowersToFollowings.follower_id == requested_user.id
        ).first()

        if followers_to_followings_record:
            return True
        else:
            return False

    def add_user_into_followers(
        self,
        *,
        target_user: Optional[Union[User, Profile]],
        requested_user: Optional[Union[User, Profile]]
    ) -> None:

        followers_to_followings_record = FollowersToFollowings()

        followers_to_followings_record.follower_id = requested_user.id
        followers_to_followings_record.following_id = target_user.id

        self.db.add(followers_to_followings_record)
        self.db.commit()
        self.db.refresh(followers_to_followings_record)

    def remove_user_from_followers(
        self,
        *,
        target_user: Optional[Union[User, Profile]],
        requested_user: Optional[Union[User, Profile]]
    ) -> None:

        q = self.db.query(FollowersToFollowings)

        q = q.filter(
            FollowersToFollowings.following_id == target_user.id
        )

        followers_to_followings_record = q.filter(
            FollowersToFollowings.follower_id == requested_user.id
        ).first()

        if not followers_to_followings_record:
            raise UserIsNotFollowed

        self.db.delete(followers_to_followings_record)
        self.db.commit()

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def get_profile_by_id(
        self, *, id: int,
        requested_user: Optional[Union[User, Profile]]
    ) -> Optional[Union[User, Profile]]:

        user = self.get(id)

        if not user:
            return None

        profile = Profile(**user.__dict__)

        if requested_user:
            profile.following = self.repository.is_user_following_for_another(
                target_user=user,
                requested_user=requested_user,
            )
        return profile
