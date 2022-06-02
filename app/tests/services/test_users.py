from unittest.mock import patch

import pytest
from sqlalchemy import exc

from app.models import User
from app.schemas.users import UserCreate, UserUpdate
from app.services.users import UserServices
from app.services.exceptions.users import (
    UserDuplicate, UserIncorrectCredentials, UserNotFound)


@patch('app.db.repositories_cache.users.UserRedisRepository')
class TestUserServices:
    def test_get(self, mock_repo):
        repo = mock_repo()
        repo.get.side_effect = [user_expected := User(id=2022), None]

        result = UserServices(repo).get(id=2022)
        assert result == user_expected

        with pytest.raises(UserNotFound):
            UserServices(repo).get(id=0)

    def test_get_by_email(self, mock_repo):
        repo = mock_repo()

        email = "test@gapo.com.vn"

        repo.get_by_email.side_effect = [
            user_expected := User(email=email),
            None
        ]

        result = UserServices(repo).get_by_email(
            email=email)
        assert result == user_expected

        with pytest.raises(UserNotFound):
            UserServices(repo).get_by_email(email=email)

    def test_get_by_username(self, mock_repo):
        repo = mock_repo()
        repo.get_by_username.side_effect = [
            user_expected := User(username="admin"),
            None
        ]

        result = UserServices(
            repo).get_by_username(username="admin")
        assert result == user_expected

        with pytest.raises(UserNotFound):
            UserServices(repo).get_by_username(username="notexist")

    def test_create(self, mock_repo):
        repo = mock_repo()
        body = UserCreate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo.get_by_email.side_effect = [
            User(id=12),
            None,
            None
        ]
        repo.get_by_username.side_effect = [
            User(id=12),
            None,
        ]

        create_user = User(id=12)
        repo.create.return_value = create_user

        with pytest.raises(UserDuplicate):
            UserServices(repo).create(body=body)

        with pytest.raises(UserDuplicate):
            UserServices(repo).create(body=body)

        assert UserServices(repo).create(body=body) == create_user

    def test_update(self, mock_repo):
        body = UserUpdate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo = mock_repo()

        repo.get.side_effect = [
            None,
            User(id=12),
            update_user := User(id=12)
        ]

        with pytest.raises(UserNotFound):
            UserServices(repo).update(id=12, body=body)

        repo.update.side_effect = [
            exc.IntegrityError(None, None, None),
            update_user
        ]

        with pytest.raises(UserDuplicate):
            UserServices(repo).update(id=12, body=body)

        assert UserServices(repo).update(
            id=12, body=body) == update_user

    @patch('app.services.users.verify_password')
    def test_authenticate(
        self, mock_verify_password, mock_repo
    ):
        repo = mock_repo()

        email = "test@example.com"
        password = "testPassword1"
        wrong_password = "testPassword2"

        repo.get_by_email.side_effect = [
            None,
            user := User(email=email),
            user
        ]

        mock_verify_password.side_effect = [False, True]

        with pytest.raises(UserNotFound):
            UserServices(repo).get_by_email(email=email)

        with pytest.raises(UserIncorrectCredentials):
            UserServices(repo).authenticate(
                email=email, password=wrong_password)

        repo.authenticate.return_value = User(email=email)

        assert UserServices(repo).authenticate(email=email, password=password)
