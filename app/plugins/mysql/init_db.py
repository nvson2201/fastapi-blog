from sqlalchemy.orm import Session
from app import schemas

from app.db import repositories
from app.plugins.mysql import base  # noqa: F401
from app.config import settings


def init_db(db: Session) -> None:

    user = repositories.users.get_by_email(email=settings.FIRST_SUPERUSER)
    if not user:
        first_superuser = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username=settings.FIRST_SUPERUSER_USERNAME,
            is_superuser=True,
        )
        user = repositories.users.create(body=first_superuser)
