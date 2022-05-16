from sqlalchemy.orm import Session
from fastapi import Depends

from app.api.dependencies.database import get_db
from app.services.posts import PostServices
from app.db.repositories_cache.posts import PostRedisRepository
from app.db import repositories
from app.config import settings

crud_engine = PostRedisRepository(
    repositories.posts, settings.REDIS_SUFFIX_POST
)


def get_post_services(
    db: Session = Depends(get_db)
):
    return PostServices(db, crud_engine=crud_engine)
