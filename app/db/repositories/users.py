from typing import List
from typing import Any, Dict, Optional, Union


from app.utils.security import get_password_hash, verify_password
from app.db.repositories.base import BaseRepository
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UserInDB
from app.schemas.datetime import DateTime
from app.config import settings
from app.db import db


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, *, email: str) -> Optional[User]:
        q = self.db.query(User)
        q = q.filter(User.email == email)
        user = q.first()
        return user

    def get_by_username(self, *, username: str) -> Optional[User]:
        q = self.db.query(User)
        q = q.filter(User.username == username)
        user = q.first()
        return user

    def create(self, *, body: Union[UserCreate, Dict[str, Any]]) -> User:

        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        hashed_password = get_password_hash(body_dict['password'])
        created_at = settings.current_time()

        create_data = UserInDB(
            hashed_password=hashed_password,
            created_at=created_at,
            updated_at=created_at,
            **body_dict
        )

        return super().create(body=create_data)

    def update(
        self,
        user: User, *, body: Union[UserUpdate, Dict[str, Any]]
    ) -> User:

        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        if 'password' in body_dict:
            hashed_password = get_password_hash(body_dict['password'])
            body_dict['hashed_password'] = hashed_password
            del body_dict['password']

        updated_at = settings.current_time()

        update_data = UserInDB(
            updated_at=updated_at,
            **body_dict
        )

        return super().update(user, body=update_data)

    def authenticate(self, *,
                     email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def get_multi(
        self, *, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        q = self.db.query(self.model)

        if date_start is None:
            date_start = DateTime(datetime=settings.past_week())
        q = q.filter(User.created_at >= date_start.datetime)

        if date_end is None:
            date_end = DateTime(datetime=settings.current_time())

        q = q.filter(User.created_at <= date_end.datetime)
        q = q.limit(limit)
        q = q.offset(skip)

        users = q.all()

        return users


users = UserRepository(User, db)
