from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models import FollowersToFollowings, User
from app.schemas.users import UserCreate, UserUpdate
from app.db.repositories.users import UserRepository
from app.utils.security import verify_password
from app.tests.utils.utils import (
    random_email, random_password, random_lower_string)


class TestUserRepository:

    def test_get_user(self, user_repo: UserRepository,
                      random_user: User) -> None:
        user = random_user
        user_2 = user_repo.get(id=user.id)
        assert user_2
        assert user.email == user_2.email
        assert jsonable_encoder(user) == jsonable_encoder(user_2)

    def test_get_user_by_email(self, user_repo: UserRepository,
                               random_user: User) -> None:
        user = random_user
        user_2 = user_repo.get_by_email(email=user.email)
        assert user_2
        assert user.email == user_2.email
        assert jsonable_encoder(user) == jsonable_encoder(user_2)

    def test_get_user_by_username(self, user_repo: UserRepository,
                                  random_user: User) -> None:
        user = random_user
        user_2 = user_repo.get_by_username(username=user.username)
        assert user_2
        assert user.email == user_2.email
        assert jsonable_encoder(user) == jsonable_encoder(user_2)

    def test_create_user(self, user_repo: UserRepository) -> None:

        email = random_email()
        password = random_password()
        username = random_lower_string()
        user_body = UserCreate(
            email=email, password=password, username=username)

        user = user_repo.create(body=user_body)
        assert user.email == email
        assert hasattr(user, "hashed_password")

    def test_update_user(self, user_repo: UserRepository,
                         random_user: User) -> None:

        user = random_user

        new_password = random_password()
        user_body_update = UserUpdate(password=new_password)
        user_repo.update(user, body=user_body_update)

        user_2 = user_repo.get(id=user.id)
        assert user_2
        assert user.email == user_2.email
        assert verify_password(new_password, user_2.hashed_password)

    def test_user_following_another_false(self, user_repo: UserRepository,
                                          random_user: User) -> None:

        target_user = random_user
        requested_user = random_user

        assert user_repo.is_user_following_for_another(
            target_user=target_user,
            requested_user=requested_user
        ) is False

    def test_add_user_into_followers(
            self,
            db: Session,
            user_repo: UserRepository,
            random_user: User
    ) -> None:

        target_user = random_user
        requested_user = random_user

        user_repo.add_user_into_followers(
            target_user=target_user,
            requested_user=requested_user
        )

        q = db.query(FollowersToFollowings)
        q = q.filter(FollowersToFollowings.following_id == target_user.id)
        q = q.filter(FollowersToFollowings.follower_id == requested_user.id)

        record = q.first()

        assert record is not None

    def test_user_following_another_true(
            self,
            user_repo: UserRepository,
            db: Session,
            random_user: User
    ) -> None:

        target_user = random_user
        requested_user = random_user

        followers_to_followings_record = FollowersToFollowings()
        followers_to_followings_record.follower_id = requested_user.id
        followers_to_followings_record.following_id = target_user.id
        db.add(followers_to_followings_record)
        db.commit()
        db.refresh(followers_to_followings_record)

        assert user_repo.is_user_following_for_another(
            target_user=target_user,
            requested_user=requested_user,
        ) is True

    def test_check_if_user_is_active(self, user_repo: UserRepository) -> None:

        email = random_email()
        password = random_password()
        username = random_lower_string()
        user_body = UserCreate(
            email=email, password=password, username=username)

        user = user_repo.create(body=user_body)
        is_active = user_repo.is_active(user)
        assert is_active is True

    def test_check_if_user_is_active_inactive(
            self, user_repo: UserRepository
    ) -> None:

        email = random_email()
        password = random_password()
        username = random_lower_string()
        user_body = UserCreate(email=email, password=password,
                               is_active=True, username=username)
        user = user_repo.create(body=user_body)
        is_active = user_repo.is_active(user)
        assert is_active

    def test_check_if_user_is_superuser(
            self, user_repo: UserRepository) -> None:

        email = random_email()
        password = random_password()
        username = random_lower_string()
        user_body = UserCreate(email=email, password=password,
                               is_superuser=True, username=username)
        user = user_repo.create(body=user_body)
        is_superuser = user_repo.is_superuser(user)
        assert is_superuser is True

    def test_check_if_user_is_superuser_normal_user(
            self, user_repo: UserRepository) -> None:

        email = random_email()
        password = random_password()
        username = random_lower_string()
        user_body = UserCreate(
            email=email, password=password, username=username)
        user = user_repo.create(body=user_body)
        is_superuser = user_repo.is_superuser(user)
        assert is_superuser is False
