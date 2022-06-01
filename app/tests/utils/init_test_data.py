from sqlalchemy.orm import Session
from app import schemas

from app.db.repositories.users import UserRepository
from app.config import settings
from app.tests.utils.database import TestingSessionLocal, engine
from app.plugins.mysql.base_class import Base


def init_test_data(db: Session) -> None:
    users = UserRepository(db)

    user = users.get_by_email(email=settings.FIRST_SUPERUSER)
    if not user:
        first_superuser = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username=settings.FIRST_SUPERUSER_USERNAME,
            is_superuser=True,
        )

        users.create(body=first_superuser)


if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_test_data(TestingSessionLocal())
