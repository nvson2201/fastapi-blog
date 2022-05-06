from typing import List
from typing import Any, Dict, Optional, Union
import datetime

from sqlalchemy.orm import Session

from app.utils.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
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

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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
        date_start: datetime.datetime = settings.START_TIME_DEFAULT,
        date_end: datetime.datetime = settings.LOCAL_CURRENT_TIME,
    ) -> List[User]:
        return (
            db.query(self.model)
            .filter(
                User.created_date >= date_start,
                User.created_date <= date_end
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


user = CRUDUser(User)
