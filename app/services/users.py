from typing import List, Optional, Union

from app.models.users import User
from app.schemas import UserUpdate, UserCreate
from app.schemas.datetime import DateTime
from app.schemas.users import UserInDB

from app.services.exceptions.users import (
    ExtensionNotSupport, UserInactive, UserNotFound,
    UserDuplicate, UserNotSuper)
from app.utils.security import get_password_hash
from app.utils.upload_avatar import upload_avatar
from app.config import settings


class UserServices:

    def __init__(self, repository):
        self.repository = repository

    def _check_duplicate_user(self, *, body: Union[UserCreate, UserUpdate]):
        if body.email:
            user = self.repository.get_by_email(email=body.email)
            if user:
                raise UserDuplicate()

        if body.username:
            user = self.repository.get_by_username(username=body.username)
            if user:
                raise UserDuplicate()

    def get(self, id: str) -> User:
        user = self.repository.get(id)
        if not user:
            raise UserNotFound

        return user

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.repository.get_by_email(email=email)
        if not user:
            raise UserNotFound

        return user

    def get_by_username(self, username: str) -> Optional[User]:
        user = self.repository.get_by_username(username=username)
        if not user:
            raise UserNotFound

        return user

    def create(self, body: UserCreate) -> User:
        self._check_duplicate_user(body=body)

        body_dict = body.dict(exclude_unset=True)
        hashed_password = get_password_hash(body_dict['password'])
        created_at = settings.current_time()

        create_data = UserInDB(
            hashed_password=hashed_password,
            created_at=created_at,
            updated_at=created_at,
            **body_dict
        )

        user = self.repository.create(body=create_data)

        return user

    def update(self, id: str, body: UserUpdate) -> User:
        user = self.repository.get(id)

        if not user:
            raise UserNotFound

        self._check_duplicate_user(body=body)

        body_dict = body.dict(exclude_unset=True)

        if 'password' in body_dict:
            hashed_password = get_password_hash(body_dict['password'])
            body_dict['hashed_password'] = hashed_password
            del body_dict['password']

        update_data = UserInDB(
            updated_at=settings.current_time(),
            **body_dict
        )
        user = self.repository.update(user, body=update_data)

        return user

    def remove(self, *, id: int):
        user = self.repository.get(id=id)
        if not user:
            raise UserNotFound
        self.repository.remove(id=id)
        return user

    def get_multi(
        self, offset: int = 0, limit: int = 100,
        date_start: DateTime = None,
        date_end: DateTime = None,
    ) -> List[User]:

        users = self.repository.get_multi(
            offset=offset, limit=limit,
            date_start=date_start,
            date_end=date_end
        )

        return users

    def is_active(self, user: User) -> bool:
        if not user.is_active:
            raise UserInactive
        return user

    def is_superuser(self, user: User) -> bool:
        if not user.is_superuser:
            raise UserNotSuper
        return user

    async def upload_user_avatar(self, *, user_id, file):
        user = self.repository.get(user_id)
        if not user:
            raise UserNotFound

        filename = await upload_avatar(file)
        if not filename:
            raise ExtensionNotSupport

        self.repository.upload_user_avatar(user=user, filename=filename)
