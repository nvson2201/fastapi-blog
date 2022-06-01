from typing import Optional

import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient

from app.db.repositories.posts import PostRepository
from app.db.repositories.users import UserRepository
from app.main import app
from app.db.db import get_db
from app.plugins.redis.services import redis_services
from sqlalchemy.orm import Session
from app.models.users import User
from app.tests.utils.posts import create_random_post
from app.tests.utils.users import create_random_user
from app.tests.utils.database import engine, TestingSessionLocal


@pytest.fixture(scope="session")
def db():
    redis_services.flush_all()

    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @sa.event.listens_for(db, "after_transaction_end")
    def end_savepoint(db, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield db

    db.close()
    transaction.rollback()
    connection.close()

    redis_services.flush_all()


@pytest.fixture(scope="class")
def client(db):

    def override_get_db():
        yield db

    # Dependency override
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="class")
def user_repo(db: Session) -> UserRepository:
    return UserRepository(db)


@pytest.fixture(scope="class")
def post_repo(db: Session) -> PostRepository:
    return PostRepository(db)


@pytest.fixture(scope="class")
def random_user(user_repo: UserRepository) -> User:
    return create_random_user(user_repo)


@pytest.fixture(scope="class")
def random_post(
        user_repo: UserRepository,
        post_repo: PostRepository,
        author_id: Optional[int] = None
) -> User:
    return create_random_post(user_repo, post_repo, author_id=author_id)
