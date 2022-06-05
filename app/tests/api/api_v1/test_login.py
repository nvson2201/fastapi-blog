from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest
from app.api.dependencies.services import get_login_services
from app.main import app
from app.config import settings
from app.services.exceptions.users import (
    UserNotFound, UserInactive, UserIncorrectCredentials)
from app.services.exceptions.tokens import InvalidToken


@pytest.fixture
def login_services():
    mock_login_services = MagicMock()
    app.dependency_overrides[get_login_services] = lambda: mock_login_services
    yield mock_login_services
    app.dependency_overrides = {}


class TestUserLogin:
    def test_get_access_token(
            self, login_services, client: TestClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }

        login_services.login_access_token.return_value = {
            "access_token": "123",
            "token_type": "bearer"
        }

        r = client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data)

        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    def test_get_access_token_incorrect_credentials(
            self, login_services, client: TestClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": "wrongpassword",
        }

        login_services.login_access_token.side_effect = \
            UserIncorrectCredentials()

        r = client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data)
        print(r)
        assert r.status_code == 400
        content = r.json()
        assert content["detail"] == "Incorrect email or password"

    def test_get_access_token_inactive(
            self, login_services, client: TestClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }

        login_services.login_access_token.side_effect = \
            UserInactive()

        r = client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data)

        assert r.status_code == 403
        content = r.json()
        assert content["detail"] == "Inactives user"

    def test_recover_password(
            self, login_services, client: TestClient
    ) -> None:
        email = settings.FIRST_SUPERUSER

        login_services.recover_password.return_value = MagicMock()

        r = client.post(
            f"{settings.API_V1_STR}/password-recovery/{email}"
        )

        assert r.status_code == 200
        content = r.json()
        assert content["msg"] == "Password recovery email sent"

    def test_recover_password_not_found(
            self, login_services, client: TestClient
    ) -> None:
        email = settings.FIRST_SUPERUSER

        login_services.recover_password.side_effect = UserNotFound()

        r = client.post(
            f"{settings.API_V1_STR}/password-recovery/{email}"
        )

        assert r.status_code == 404
        content = r.json()
        assert content["detail"] == (
            "The user with this username does not exist in the system.")

    def test_reset_password(
            self, login_services, client: TestClient
    ) -> None:
        data = {
            "body": "1aaAAAAAAAAA",
            "token": "1"
        }
        login_services.reset_password.return_value = 100

        r = client.post(
            f"{settings.API_V1_STR}/reset-password", json=data)

        assert r.status_code == 200
        content = r.json()
        assert content["msg"] == "Password updated successfully"

    def test_reset_password_invalid_token(
            self, login_services, client: TestClient
    ) -> None:
        data = {
            "body": "1aaAAAAAAAAA",
            "token": "1"
        }
        login_services.reset_password.side_effect = InvalidToken()

        r = client.post(
            f"{settings.API_V1_STR}/reset-password", json=data)

        assert r.status_code == 401
        content = r.json()
        assert content["detail"] == "Invalid token"

    def test_reset_password_user_not_found(
            self, login_services, client: TestClient
    ) -> None:
        data = {
            "body": "1aaAAAAAAAAA",
            "token": "1"
        }
        login_services.reset_password.side_effect = UserNotFound()

        r = client.post(
            f"{settings.API_V1_STR}/reset-password", json=data)

        assert r.status_code == 404
        content = r.json()
        assert content["detail"] == (
            "The user with this username does not exist in the system.")

    def test_reset_password_user_inactive(
            self, login_services, client: TestClient
    ) -> None:
        data = {
            "body": "1aaAAAAAAAAA",
            "token": "1"
        }
        login_services.reset_password.side_effect = UserInactive()

        r = client.post(
            f"{settings.API_V1_STR}/reset-password", json=data)

        assert r.status_code == 403
        content = r.json()
        assert content["detail"] == "Inactive user"
