from sqlalchemy.orm import Session

from fastapi import Depends
from typing import Any, Type
from app.db.repositories.base import BaseRepository
from app.db.repositories_cache.base import RedisDecorator
from app.db.db import get_db


def get_redis_repo(
    repo_redis_type: Type[RedisDecorator],
    repo_type: Type[BaseRepository],
) -> Any:

    def _get_redis_repo(db: Session = Depends(get_db)) -> Any:
        return repo_redis_type(db, repo_type(db))

    return _get_redis_repo
