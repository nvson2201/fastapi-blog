from typing import Dict

from fastapi.testclient import TestClient

from app.config import settings
from app.models.users import User
from app.schemas.users import UserCreate
from app.db.repositories.users import UserRepository
from app.tests.utils.utils import (
    random_email, random_password, random_lower_string)


class TestSuperUserAPI:

    def test_get_users_superuser_me(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ) -> None:
        r = client.get(f"{settings.API_V1_STR}/users/me",
                       headers=superuser_token_headers)
        current_user = r.json()
        assert current_user
        assert current_user["is_active"] is True
        assert current_user["is_superuser"]
        assert current_user["email"] == settings.FIRST_SUPERUSER

    def test_create_user_new_email(
        self, client: TestClient, superuser_token_headers: dict,
        user_repo: UserRepository
    ) -> None:
        email = random_email()

        password = random_password()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300

        created_user = r.json()
        user2 = user_repo.get_by_email(email=email)

        assert user2
        assert user2.email == created_user["email"]

    def test_get_existing_user(
        self,
        client: TestClient, superuser_token_headers: dict,
        user_repo: UserRepository,
        random_user: User
    ) -> None:

        user = random_user
        print("request ID", user.id)
        r = client.get(
            f"{settings.API_V1_STR}/users/{user.id}",
            headers=superuser_token_headers,
        )

        assert 200 <= r.status_code < 300
        api_user = r.json()
        print("response", api_user)

        existing_user = user_repo.get_by_email(email=user.email)
        print("with email ID", existing_user.__dict__)
        assert existing_user
        assert existing_user.email == api_user["email"]

    def test_create_user_existing_username(
        self,
        client: TestClient, superuser_token_headers: dict,
        user_repo: UserRepository
    ) -> None:
        email = random_email()
        password = random_password()
        username = random_lower_string()
        user_body = UserCreate(
            email=email, password=password, username=username)
        user_repo.create(body=user_body)

        data = {"email": email, "password": password, "username": username}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers, json=data,
        )
        created_user = r.json()
        assert r.status_code == 409
        assert "_id" not in created_user

    def test_retrieve_users(
        self,
        client: TestClient, superuser_token_headers: dict,
        random_user: User
    ) -> None:

        random_user
        random_user

        r = client.get(f"{settings.API_V1_STR}/users/",
                       headers=superuser_token_headers)
        all_users = r.json()

        assert len(all_users) > 1
        for item in all_users:
            assert "email" in item

    def test_read_user(
        self,
        client: TestClient, superuser_token_headers: dict,
        random_user: User
    ) -> None:
        user = random_user
        response = client.get(
            f"{settings.API_V1_STR}/users/{user.id}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["email"] == user.email
        assert content["id"] == user.id
        assert content["is_active"] == user.is_active
