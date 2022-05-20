from fastapi.encoders import jsonable_encoder

from app.db.repositories import users
from app.utils.security import verify_password
from app.schemas.users import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_password


def test_create_user() -> None:
    email = random_email()
    password = random_password()
    user_body = UserCreate(email=email, password=password)
    user = users.create(body=user_body)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user() -> None:
    email = random_email()
    password = random_password()
    user_body = UserCreate(email=email, password=password)
    user = users.create(body=user_body)
    authenticated_user = users.authenticate(
        email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user() -> None:
    email = random_email()
    password = random_password()
    user = users.authenticate(email=email, password=password)
    assert user is None


def test_check_if_user_is_active() -> None:
    email = random_email()
    password = random_password()
    user_body = UserCreate(email=email, password=password)
    user = users.create(body=user_body)
    is_active = users.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive() -> None:
    email = random_email()
    password = random_password()
    user_body = UserCreate(email=email, password=password, is_active=True)
    user = users.create(body=user_body)
    is_active = users.is_active(user)
    assert is_active


def test_check_if_user_is_superuser() -> None:
    email = random_email()
    password = random_password()
    user_body = UserCreate(email=email, password=password, is_superuser=True)
    user = users.create(body=user_body)
    is_superuser = users.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user() -> None:
    username = random_email()
    password = random_password()
    user_body = UserCreate(email=username, password=password)
    user = users.create(body=user_body)
    is_superuser = users.is_superuser(user)
    assert is_superuser is False


def test_get_user() -> None:
    password = random_password()
    username = random_email()
    user_body = UserCreate(
        email=username, password=password, is_superuser=True)
    user = users.create(body=user_body)
    user_2 = users.get(id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user() -> None:
    password = random_password()
    email = random_email()
    user_body = UserCreate(email=email, password=password, is_superuser=True)
    user = users.create(body=user_body)
    new_password = random_password()
    user_body_update = UserUpdate(password=new_password, is_superuser=True)
    users.update(user, body=user_body_update)
    user_2 = users.get(id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
