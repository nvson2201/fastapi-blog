from sqlalchemy.orm import Session
from fastapi import Depends

from app.api.dependencies.database import get_db
from app.services.user import UserServices
from app.db.repositories_cache.user import CRUDRedisUserDecorator
from app.db import repositories
from app.config import settings

crud_engine = CRUDRedisUserDecorator(
    repositories.user, settings.REDIS_SUFFIX_USER
)


def get_user_services(
    db: Session = Depends(get_db)
):
    return UserServices(db, crud_engine=crud_engine)
