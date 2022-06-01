from typing import Dict

import pytest

from app.db.repositories.users import UserRepository
from fastapi.testclient import TestClient
from app.config import settings
from app.tests.utils.users import (
    authentication_token_from_email, get_superuser_token_headers)


@pytest.fixture(scope="class")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="class")
def normal_user_token_headers(
    client: TestClient, user_repo: UserRepository
) -> Dict[str, str]:
    return authentication_token_from_email(
        user_repo=user_repo, client=client, email=settings.EMAIL_TEST_USER
    )
