from unittest.mock import patch, sentinel

import pytest

from app.models import User
from app.schemas.users import UserCreate, UserUpdate
from app.services.users import UserServices
from app.services.exceptions.users import (
    UserDuplicate, UserIncorrectCredentials, UserNotFound)


@patch('app.db.repositories_cache.users.UserRedisRepository')
class TestUserServices:
    def test_get(self, repo):
        repo.get.side_effect = [sentinel.user]
        result = UserServices(repo).get(id=2022)

        assert result == sentinel.user

    def test_get_fail(self, repo):
        repo.get.side_effect = [None]

        with pytest.raises(UserNotFound):
            UserServices(repo).get(id=0)

    def test_get_by_email(self, repo):
        email = "test@gapo.com.vn"
        repo.get_by_email.side_effect = [sentinel.user]
        result = UserServices(repo).get_by_email(email=email)

        assert result == sentinel.user

    def test_get_by_email_fail(self, repo):
        email = "test@gapo.com.vn"
        repo.get_by_email.side_effect = [None]

        with pytest.raises(UserNotFound):
            UserServices(repo).get_by_email(email=email)

    def test_get_by_username(self, repo):
        repo.get_by_username.side_effect = [sentinel.user]
        result = UserServices(repo).get_by_username(username="admin")

        assert result == sentinel.user

    def test_get_by_username_fail(self, repo):
        repo.get_by_username.side_effect = [None]

        with pytest.raises(UserNotFound):
            UserServices(repo).get_by_username(username="notexist")

    @patch.object(UserServices, 'send_code', autospec=True)
    def test_create(self, send_code, repo):
        sentinel.user = User()
        body = UserCreate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo.get_by_email.side_effect = [None]
        repo.get_by_username.side_effect = [None]
        repo.create.return_value = sentinel.user
        send_code.side_effect = [None]

        assert UserServices(repo).create(body=body) == sentinel.user

    def test_create_user_same_email(self, repo):
        sentinel.user
        body = UserCreate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo.get_by_email.return_value = sentinel.user
        sentinel.user.is_active = True

        with pytest.raises(UserDuplicate):
            UserServices(repo).create(body=body)

    def test_create_user_same_username(self, repo):
        sentinel.user = User()
        body = UserCreate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo.get_by_email.return_value = None
        repo.get_by_username.return_value = sentinel.user
        sentinel.user.is_active = True

        with pytest.raises(UserDuplicate):
            UserServices(repo).create(body=body)

    def test_update(self, repo):
        body = UserUpdate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo.get.side_effect = [sentinel.user]
        repo.update.side_effect = [sentinel.user]
        repo.get_by_email.side_effect = [None]
        repo.get_by_username.side_effect = [None]

        assert UserServices(repo).update(
            id=12, body=body) == sentinel.user

    def test_update_not_found_user(self, repo):
        body = UserUpdate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )
        repo.get.side_effect = [None]

        with pytest.raises(UserNotFound):
            UserServices(repo).update(id=12, body=body)

    def test_update_duplicate_user(self, repo):
        body = UserUpdate(
            username="test",
            email="test@example.com",
            password="testPassword1"
        )

        repo.get.side_effect = [sentinel.user]

        with pytest.raises(UserDuplicate):
            UserServices(repo).update(id=12, body=body)

    @patch('app.services.users.verify_password')
    def test_authenticate(
        self, mock_verify_password, repo
    ):
        email = "test@example.com"
        password = "testPassword1"
        sentinel.user = User()

        repo.get_by_email.side_effect = [sentinel.user]
        mock_verify_password.side_effect = [True]

        repo.authenticate.return_value = User(email=email)

        assert UserServices(repo).authenticate(email=email, password=password)

    def test_authenticate_not_found_user(self, repo):
        email = "test@example.com"
        password = "testPassword1"
        repo.get_by_email.side_effect = [None]

        with pytest.raises(UserNotFound):
            UserServices(repo).authenticate(email=email, password=password)

    @patch('app.services.users.verify_password')
    def test_authenticate_wrong_password(self, mock_verify_password, repo):
        email = "test@example.com"
        wrong_password = "testPassword2"
        sentinel.user = User()

        repo.get_by_email.side_effect = [sentinel.user]
        mock_verify_password.side_effect = [False]

        with pytest.raises(UserIncorrectCredentials):
            UserServices(repo).authenticate(
                email=email, password=wrong_password)

    def test_remove_user_not_found(self, repo):
        repo.get.side_effect = [None]
        with pytest.raises(UserNotFound):
            UserServices(repo).remove(id=1)
