from app.plugins.redis import redis_services
from sqlalchemy.orm import Session
from app.config import settings
from app import crud
from app.models.user import User
from app.schemas.user import UserUpdate, UserCreate
from .exceptions import UserNotFound, UserDuplicate, UserForbiddenRegiser
from sqlalchemy import exc
from app.utils.mail import send_new_account_email


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
            if not user:
                raise UserNotFound

            self._set_cache(id=id, data=user)

        return user

    def update_by_id(self, db: Session, id: str, body: UserUpdate):
        user = self.get_by_id(db, id=id)
        if not user:
            raise UserNotFound

        try:
            user = crud.user.update(db, db_obj=user, obj_in=body)
        except exc.IntegrityError:
            raise UserDuplicate

        self._set_cache(id=user.id, data=user)

        return user

    def create_user(self, db: Session, body: UserCreate):
        user = crud.user.get_by_email(db, email=body.email)
        if user:
            raise UserDuplicate
        user = crud.user.create(db, obj_in=body)
        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        self._set_cache(id=user.id, data=user)

        return user

    def create_user_open(self, db: Session, body: UserCreate):
        if not settings.USERS_OPEN_REGISTRATION:
            raise UserForbiddenRegiser
        user = crud.user.get_by_email(db, email=body.email)
        if user:
            raise UserDuplicate
        user = crud.user.create(db, obj_in=body)
        if settings.EMAILS_ENABLED and body.email:
            send_new_account_email(
                email_to=body.email,
                username=body.email,
                password=body.password
            )

        self._set_cache(id=user.id, data=user)

        return user

    def read_users(self, db: Session, skip: int = 0, limit: int = 100):
        users = crud.user.get_multi(db, skip=skip, limit=limit)
        return users
