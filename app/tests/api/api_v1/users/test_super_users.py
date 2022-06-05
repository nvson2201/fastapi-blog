import pytest
from fastapi.testclient import TestClient

from app.tests.utils.utils import (
    random_email, random_password, random_lower_string)
from app.services.exceptions.users import UserDuplicate, UserNotFound
from app.config import settings
from app.tests.utils.users import random_user


class TestSuperUserAPI:

    @pytest.mark.usefixtures("override_superuser")
    def test_get_users_superuser_me(
        self, client: TestClient
    ) -> None:
        r = client.get(f"{settings.API_V1_STR}/users/me",
                       headers={})

        current_user = r.json()
        assert current_user
        assert current_user["is_active"] is True
        assert current_user["is_superuser"]
        assert current_user["email"] == settings.FIRST_SUPERUSER

    @ pytest.mark.usefixtures("override_superuser")
    def test_create_user_new_email(
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

        user_services.create.return_value = user

        r = client.post(
            f"{settings.API_V1_STR}/users/", headers={}, json=data,
        )

        assert 200 <= r.status_code < 300
        created_user = r.json()
        assert user.email == created_user["email"]

    @pytest.mark.usefixtures("override_superuser")
    def test_create_user_existing_username(
        self,
        user_services,
        client: TestClient
    ) -> None:
        email = random_email()
        password = random_password()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}

        user_services.create.side_effect = UserDuplicate()
        r = client.post(
            f"{settings.API_V1_STR}/users/", headers={}, json=data,
        )

        created_user = r.json()
        assert r.status_code == 409
        assert "_id" not in created_user

    @pytest.mark.usefixtures("override_superuser")
    def test_retrieve_users(
        self,
        user_services,
        client: TestClient
    ) -> None:
        user_services.get_multi.return_value = [random_user(), random_user()]

        r = client.get(f"{settings.API_V1_STR}/users/", headers={})

        all_users = r.json()

        assert len(all_users) > 1
        for item in all_users:
            assert "email" in item

    @pytest.mark.usefixtures("override_superuser")
    def test_read_user(
        self,
        user_services,
        client: TestClient
    ) -> None:
        user = random_user()
        user_services.get.return_value = user
        response = client.get(
            f"{settings.API_V1_STR}/users/{user.id}",
            headers={},
        )

        assert response.status_code == 200
        content = response.json()
        assert content["email"] == user.email
        assert content["id"] == user.id
        assert content["is_active"] == user.is_active

    @pytest.mark.usefixtures("override_superuser")
    def test_read_user_not_found(
        self,
        user_services,
        client: TestClient
    ) -> None:
        user = random_user()
        user_services.get.side_effect = UserNotFound()
        r = client.get(
            f"{settings.API_V1_STR}/users/{user.id}",
            headers={},
        )

        assert r.status_code == 404
        content = r.json()
        assert content["detail"] == "User not found"

    @ pytest.mark.usefixtures("override_superuser")
    def test_update_user_new_email(
        self,
        user_services,
        client: TestClient,
    ) -> None:
        email = random_email()
        data = {"email": email}

        user = random_user()
        user.email = email

        user_services.update.return_value = user

        r = client.put(
            f"{settings.API_V1_STR}/users/{user.id}", headers={}, json=data,
        )

        assert 200 <= r.status_code < 300
        updated_user = r.json()
        assert user.email == updated_user["email"]

    @ pytest.mark.usefixtures("override_superuser")
    def test_update_user_not_found_user(
        self,
        user_services,
        client: TestClient,
    ) -> None:
        email = random_email()
        data = {"email": email}

        user = random_user()
        user.email = email

        user_services.update.side_effect = UserNotFound()

        r = client.put(
            f"{settings.API_V1_STR}/users/{user.id}", headers={}, json=data,
        )

        assert r.status_code == 404
        content = r.json()
        assert content["detail"] == "User not found"

    @ pytest.mark.usefixtures("override_superuser")
    def test_update_user_existing_email(
        self,
        user_services,
        client: TestClient,
    ) -> None:
        email = random_email()
        data = {"email": email}

        user = random_user()
        user.email = email

        user_services.update.side_effect = UserDuplicate()

        r = client.put(
            f"{settings.API_V1_STR}/users/{user.id}", headers={}, json=data,
        )

        assert r.status_code == 409
        content = r.json()
        assert content["detail"] == "User with this email already exists"
