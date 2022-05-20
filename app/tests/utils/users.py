from typing import Dict
from app.db.repositories import users

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_password


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_password()
    user_body = UserCreate(email=email, password=password)
    user = users.create(body=user_body)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_password()
    user = users.get_by_email(email=email)
    if not user:
        user_update_body = UserCreate(email=email, password=password)
        user = users.create(body=user_update_body)
    else:
        user_update_body = UserUpdate(password=password)
        user = users.update(user, body=user_update_body)

    return user_authentication_headers(
        client=client, email=email, password=password)
