import pytest
from fastapi.testclient import TestClient
from app.services.exceptions.users import UserDuplicate
from app.tests.utils.users import random_user

from app.tests.utils.utils import (
    random_email, random_lower_string, random_password)
from app.config import settings
from app.utils.security import get_password_hash


class TestNormalUserAPI:
    @pytest.mark.usefixtures("override_user")
    def test_get_users_normal_user_me(self, client: TestClient) -> None:

        r = client.get(f"{settings.API_V1_STR}/users/me", headers={})

        current_user = r.json()
        assert current_user
        assert current_user["is_active"] is True
        assert current_user["is_superuser"] is False
        assert current_user["email"] == settings.EMAIL_TEST_USER

    @pytest.mark.usefixtures("override_user")
    def test_create_user_by_normal_user(
        self, client: TestClient
    ) -> None:
        email = random_email()
        password = random_password()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}

        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers={}, json=data,
        )
        assert r.status_code == 403

    @pytest.mark.usefixtures("override_user")
    def test_update_user_me(
        self,
        user_services,
        client: TestClient,
    ) -> None:
        email = random_email()
        password = random_password()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}

        user = random_user()
        user.email = email
        user.username = username
        user.hashed_password = get_password_hash(random_password())

        user_services.update.return_value = user

        r = client.put(
            f"{settings.API_V1_STR}/users/me", headers={}, json=data,
        )

        assert 200 <= r.status_code < 300
        created_user = r.json()
        assert user.email == created_user["email"]

    @pytest.mark.usefixtures("override_user")
    def test_update_user_me_existing_email(
        self,
        user_services,
        client: TestClient,
    ) -> None:
        email = random_email()
        password = random_password()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}

        user = random_user()
        user.email = email
        user.username = username
        user.hashed_password = get_password_hash(random_password())

        user_services.update.side_effect = UserDuplicate()

        r = client.put(
            f"{settings.API_V1_STR}/users/me", headers={}, json=data,
        )

        assert r.status_code == 409
        content = r.json()
        assert content["detail"] == "User with this email already exists"
