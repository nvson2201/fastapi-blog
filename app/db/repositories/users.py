from typing import List
from typing import Optional, Union

from app.schemas.users import UserCreate, UserUpdate
from app.schemas.profiles import Profile
from app.schemas.datetime import DateTime
from app.models.users import User
from app.models.followers_to_followings import FollowersToFollowings
from app.services.exceptions.profile import UserIsNotFollowed
from app.db.repositories.base import BaseRepository
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

        follower_to_following = q.filter(
            FollowersToFollowings.following_id == target_user.id,
            FollowersToFollowings.follower_id == requested_user.id
        ).first()

        return bool(follower_to_following)

    def add_follower_to_following(
        self, *, follower_to_following: FollowersToFollowings
    ) -> None:

        self.db.add(follower_to_following)
        self.db.commit()
        self.db.refresh(follower_to_following)

    def remove_user_from_followers(
        self,
        *,
        target_user: Optional[Union[User, Profile]],
        requested_user: Optional[Union[User, Profile]]
    ) -> None:

        follower_to_following = self.db.query(
            FollowersToFollowings
        ).filter(
            FollowersToFollowings.following_id == target_user.id,
            FollowersToFollowings.follower_id == requested_user.id
        ).first()

        if not follower_to_following:
            raise UserIsNotFollowed

        self.db.delete(follower_to_following)
        self.db.commit()
