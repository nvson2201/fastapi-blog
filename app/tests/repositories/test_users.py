from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from app.config import settings

from app.models import FollowersToFollowings, User
from app.schemas.users import UserInDB
from app.db.repositories.users import UserRepository
from app.tests.utils.utils import random_password
from app.tests.utils.users import random_user
from app.utils.security import get_password_hash


class TestUserRepository:

    def test_get_user(self) -> None:
        id = 1
        db = UnifiedAlchemyMagicMock()

        UserRepository(db).get(id=id)

        db.query.assert_called_once_with(User)
        db.filter.assert_called_once_with(User.id == id)

    def test_get_user_by_email(self):
        email = "nguyenvanson@gapo.com.vn"
        db = UnifiedAlchemyMagicMock()

        UserRepository(db).get_by_email(email=email)

        db.query.assert_called_once_with(User)
        db.filter.assert_called_once_with(User.email == email)

    def test_get_user_by_username(self):
        username = "admin"
        db = UnifiedAlchemyMagicMock()

        UserRepository(db).get_by_username(username=username)

        db.query.assert_called_once_with(User)
        db.filter.assert_called_once_with(User.username == username)

    def test_create_user(self):
        db = UnifiedAlchemyMagicMock()

        email = "nguyenvanson@gapo.com.vn"
        hashed_password = get_password_hash("string11A")
        username = "admin"
        created_at = settings.current_time()
        user_body = UserInDB(
            email=email,
            username=username,
            hashed_password=hashed_password,
            created_at=created_at,
            updated_at=created_at,
        )

        UserRepository(db).create(body=user_body)

        db.add.assert_called()
        db.refresh.assert_called()
        db.commit.assert_called()

    def test_update_user(self):
        db = UnifiedAlchemyMagicMock()
        user = random_user()

        user_body_update = UserInDB(
            updated_at=settings.current_time(),
            hashed_password=get_password_hash(random_password())
        )
        UserRepository(db).update(user, body=user_body_update)

        db.merge.assert_called()
        db.commit.assert_called()

    def test_add_follower_to_following(self):
        db = UnifiedAlchemyMagicMock()

        target_user = random_user()
        requested_user = random_user()

        follower_to_following = FollowersToFollowings(
            follower_id=requested_user.id,
            following_id=target_user.id
        )

        UserRepository(db).add_follower_to_following(
            follower_to_following=follower_to_following
        )

        db.add.assert_called_once_with(follower_to_following)
        db.commit.assert_called_once_with()
        db.refresh.assert_called_once_with(follower_to_following)

    def test_user_following_another_true(self):
        db = UnifiedAlchemyMagicMock()
        target_user = random_user()
        requested_user = random_user()

        db.query.return_value.filter.return_value.first.side_effect = \
            [FollowersToFollowings(
                following_id=target_user.id,
                follower_id=requested_user.id
            )]

        result = UserRepository(db).is_user_following_for_another(
            target_user=target_user,
            requested_user=requested_user,
        )

        db.query.assert_called_once_with(FollowersToFollowings)
        db.filter.assert_called_once_with(
            FollowersToFollowings.following_id == target_user.id,
            FollowersToFollowings.follower_id == requested_user.id
        )

        assert result is True

    def test_user_following_another_false(self):
        db = UnifiedAlchemyMagicMock()
        target_user = random_user()
        requested_user = random_user()

        db.query.return_value.filter.return_value.first.side_effect = [None]

        result = UserRepository(db).is_user_following_for_another(
            target_user=target_user,
            requested_user=requested_user,
        )

        db.query.assert_called_once_with(FollowersToFollowings)
        db.filter.assert_called_once_with(
            FollowersToFollowings.following_id == target_user.id,
            FollowersToFollowings.follower_id == requested_user.id
        )

        assert result is False
