from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.models.users import User
from app.api.dependencies.services import get_user_services
from app.api.dependencies.authentication import (
    get_current_active_superuser, get_current_active_user)
from app.config import settings


@pytest.fixture(scope="class")
def client():
    yield TestClient(app)


def super_user():
    return User(
        id=1,
        is_active=True,
        is_superuser=True,
        email=settings.FIRST_SUPERUSER
    )


@pytest.fixture(scope="class")
def override_superuser():
    app.dependency_overrides[get_current_active_superuser] = super_user
    app.dependency_overrides[get_current_active_user] = super_user
    yield
    app.dependency_overrides = {}


def permission_error():
    raise HTTPException(
        status_code=403,
        detail="Not enough permissions"
    )


def normal_user():
    return User(
        id=1,
        is_active=True,
        is_superuser=False,
        email=settings.EMAIL_TEST_USER
    )


@pytest.fixture(scope="class")
def override_user():
    app.dependency_overrides[get_current_active_user] = normal_user
    app.dependency_overrides[get_current_active_superuser] = permission_error
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="class")
def user_services():
    mock_user_services = MagicMock()
    app.dependency_overrides[get_user_services] = lambda: mock_user_services
    yield mock_user_services
    app.dependency_overrides = {}
