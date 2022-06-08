from unittest.mock import patch, sentinel

import pytest

from app.models import User
from app.services.login import LoginServices
from app.services.exceptions.users import (
    UserIncorrectCredentials, UserNotFound)


@ patch('app.services.users.UserServices')
@ patch('app.db.repositories_cache.users.UserRedisRepository')
class TestLoginServices:
    @ patch.object(LoginServices, 'authenticate', autospec=True)
    @ patch('app.services.login.verify_password')
    def test_authenticate(
        self, mock_verify_password, authenticate, repo, user_services
    ):
        email = "test@example.com"
        password = "testPassword1"
        sentinel.user = User()

        repo.get_by_email.side_effect = [sentinel.user]
        mock_verify_password.side_effect = [True]

        authenticate.return_value = User(email=email)

        assert LoginServices(repo, user_services).authenticate(
            email=email, password=password)

    def test_authenticate_not_found_user(self, repo, user_services):
        email = "test@example.com"
        password = "testPassword1"
        repo.get_by_email.side_effect = [None]

        with pytest.raises(UserNotFound):
            LoginServices(repo, user_services).authenticate(
                email=email, password=password)

    @patch('app.services.login.verify_password')
    def test_authenticate_wrong_password(
            self, mock_verify_password,
            repo, user_services
    ):
        email = "test@example.com"
        wrong_password = "testPassword2"
        sentinel.user = User()

        repo.get_by_email.side_effect = [sentinel.user]
        mock_verify_password.side_effect = [False]

        with pytest.raises(UserIncorrectCredentials):
            LoginServices(repo, user_services).authenticate(
                email=email, password=wrong_password)
