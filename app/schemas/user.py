from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str

    @validator('password')
    def password_validate(cls, v):
        if len(v) < 8:
            raise ValueError('Length should be at least 8')

        if not any(char.isdigit() for char in v):
            raise ValueError('Password should have at least one numeral')

        if not any(char.islower() for char in v):
            raise ValueError(
                'Password should have at least one lowercase letter')

        return v


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
