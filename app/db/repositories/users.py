from typing import List
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.utils.security import get_password_hash, verify_password
from app.db.repositories.base import BaseRepository
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.schemas.datetime import DateTime
from app.config import settings


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, body: UserCreate) -> User:
        user = User()
        exclude_keys_in_user_model = ['password', 'created_at']

        for key, value in body.__dict__.items():
            if key not in exclude_keys_in_user_model:
                setattr(user, key, value)

        user.hashed_password = get_password_hash(body.password)
        user.created_at = settings.current_time()

        return super().create(db, body=user)

    def update(
        self, db: Session,
        user: User, *, body: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(body, dict):
            update_data = body
        else:
            update_data = body.dict(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, user=user, body=update_data)

    def authenticate(self, db: Session, *,
                     email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
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
        self, db: Session, *, skip: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        q = db.query(self.model)

        if date_start is None:
            date_start = DateTime(datetime=settings.past_week())
        q = q.filter(User.created_at >= date_start.datetime)

        if date_end is None:
            date_end = DateTime(datetime=settings.current_time())
        q = q.filter(User.created_at <= date_end.datetime)

        q = q.limit(limit)
        q = q.offset(skip)

        return q.all()


users = UserRepository(User)
