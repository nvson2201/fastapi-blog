from app.plugins.redis import redis_services
from sqlalchemy.orm import Session
from app.config import settings
from app import crud
from app.models.user import User


class UserCL:
    def get(self, id: str):
        return redis_services.get_cache(
            id=str(id),
            suffix=settings.REDIS_SUFFIX_USER
        )

    def set(self, id: str, data: User):
        redis_services.set_cache(
            id=str(id),
            suffix=settings.REDIS_SUFFIX_USER,
            data=data.__dict__
        )

    def get_or_set(self, db: Session, id: str):
        cache_data = self.get(id=id)

        if cache_data:
            user = User(**cache_data)
        else:
            user = crud.user.get(db, id=id)
            cache_data = self.set(id=id, data=user)

        return user


user = UserCL()
