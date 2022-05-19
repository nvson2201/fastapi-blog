from app.api.dependencies.database import get_db
from app.services.users import UserServices
from app.db.repositories_cache.users import UserRedisRepository
from app.db import repositories
from app.config import settings

db = next(get_db())

crud_engine = UserRedisRepository(
    repositories.users, settings.REDIS_PREFIX_USER
)


def get_user_services():
    return UserServices(db, crud_engine=crud_engine)
