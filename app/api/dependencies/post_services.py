from app.api.dependencies.database import get_db
from app.services.posts import PostServices
from app.db.repositories_cache.posts import PostRedisRepository
from app.db import repositories
from app.config import settings

db = next(get_db())

crud_engine = PostRedisRepository(
    repositories.posts, settings.REDIS_PREFIX_POST
)


def get_post_services():
    return PostServices(db, crud_engine=crud_engine)
