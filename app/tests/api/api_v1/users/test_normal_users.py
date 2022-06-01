from typing import Dict

from fastapi.testclient import TestClient

from app.config import settings

from app.tests.utils.utils import random_email, random_password


class TestNormalUserAPI:

    def test_get_users_normal_user_me(
        self, client: TestClient, normal_user_token_headers: Dict[str, str]
    ) -> None:
        r = client.get(f"{settings.API_V1_STR}/users/me",
                       headers=normal_user_token_headers)
        current_user = r.json()
        assert current_user
        assert current_user["is_active"] is True
        assert current_user["is_superuser"] is False
        assert current_user["email"] == settings.EMAIL_TEST_USER

    def test_create_user_by_normal_user(
        self,
        client: TestClient, normal_user_token_headers: Dict[str, str]
    ) -> None:
        username = random_email()
        password = random_password()

        data = {"username": username, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=normal_user_token_headers, json=data,
        )
        assert r.status_code == 403
