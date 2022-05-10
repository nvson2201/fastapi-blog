from typing import List
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.utils.security import get_password_hash, verify_password
from app.db.repositories.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.datetime import DateTime
from app.config import settings


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User()
        exclude_keys_in_user_model = ['password', 'created_date']

        for key, value in obj_in.__dict__.items():
            if key not in exclude_keys_in_user_model:
                setattr(db_obj, key, value)

        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_obj.created_date = settings.current_time()

        return super().create(db, obj_in=db_obj)

    def update(
        self, db: Session, *,
        db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

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
        q = q.filter(User.created_date >= date_start.datetime)

        if date_end is None:
            date_end = DateTime(datetime=settings.current_time())
        q = q.filter(User.created_date <= date_end.datetime)

        q = q.limit(limit)
        q = q.offset(skip)

        return q.all()


user = CRUDUser(User)
