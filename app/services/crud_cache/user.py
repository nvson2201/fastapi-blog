from app.plugins.redis import redis_services
from sqlalchemy.orm import Session
from app.config import settings
from app import crud
from app.models.user import User


class UserServices:

    def __init__(self, db: Session):
        self.db = db

    def _get_cache(self, id: str):
        return redis_services.get_cache(
            id=str(id),
            suffix=settings.REDIS_SUFFIX_USER
        )

    def _set_cache(self, id: str, data: User):
        redis_services.set_cache(
            id=str(id),
            suffix=settings.REDIS_SUFFIX_USER,
            data=data.__dict__
        )

    def get_by_id(self, db: Session, id: str):
        cache_data = self._get_cache(id=id)

        if cache_data:
            user = User(**cache_data)
        else:
            user = crud.user.get(db, id=id)
            cache_data = self._set_cache(id=id, data=user)

        return user
