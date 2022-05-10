from sqlalchemy.orm import Session
from app.plugins.mysql import schemas

from app.db import repositories
from app.plugins.mysql import base  # noqa: F401
from app.config import settings


def init_db(db: Session) -> None:

    user = repositories.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        first_superuser = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = repositories.user.create(db, obj_in=first_superuser)
