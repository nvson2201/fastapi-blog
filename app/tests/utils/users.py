from typing import Dict

from fastapi.testclient import TestClient
from app.models.users import User

from app.schemas.users import UserCreate, UserUpdate
from app.db.repositories.users import UserRepository
from app.config import settings
from app.tests.utils.utils import (
    random_email, random_password, random_lower_string)


def authentication_token_from_email(
    user_repo: UserRepository,
    *, client: TestClient, email: str
) -> Dict[str, str]:
    password = random_password()
    username = random_lower_string()
    user = user_repo.get_by_email(email=email)

    if not user:
        user_create_body = UserCreate(
            email=email, password=password, username=username)
        user = user_repo.create(body=user_create_body)
    else:

        user_update_body = UserUpdate(password=password)
        user = user_repo.update(user, body=user_update_body)

    return user_authentication_headers(
        client=client, email=email, password=password)


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def create_random_user(user_repo: UserRepository) -> User:
    email = random_email()
    password = random_password()
    username = random_lower_string()
    user_body = UserCreate(
        email=email, password=password, username=username)

    user = user_repo.create(body=user_body)
    return user
