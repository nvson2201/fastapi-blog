from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_banned: Optional[bool] = False
    is_superuser: bool = False
    full_name: Optional[str] = None
    username: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str

    @validator('full_name')
    def full_name_validator(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(
                'The full name must contain alpha characters only.'
            )

    @validator('password')
    def password_validate(cls, v):
        if len(v) < 8:
            raise ValueError('Length should be at least 8')

        if not any(char.isdigit() for char in v):
            raise ValueError('Password should have at least one numeral')

        if not any(char.isupper() for char in v):
            raise ValueError(
                'Password should have at least one uppercase letter')

        if not any(char.islower() for char in v):
            raise ValueError(
                'Password should have at least one lowercase letter')

        return v


class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None

    @validator('username')
    def full_name_validator(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(
                'The username must contain alpha characters only.'
            )

    @validator('password')
    def password_validate(cls, v):
        if len(v) < 8:
            raise ValueError('Length should be at least 8')

        if not any(char.isdigit() for char in v):
            raise ValueError('Password should have at least one numeral')

        if not any(char.isupper() for char in v):
            raise ValueError(
                'Password should have at least one uppercase letter')

        if not any(char.islower() for char in v):
            raise ValueError(
                'Password should have at least one lowercase letter')

        return v


class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):  # response_model
    pass


class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None


class UserPassword(BaseModel):
    body: str

    @validator('body')
    def password_validate(cls, v):
        if len(v) < 8:
            raise ValueError('Length should be at least 8')

        if not any(char.isdigit() for char in v):
            raise ValueError('Password should have at least one numeral')

        if not any(char.isupper() for char in v):
            raise ValueError(
                'Password should have at least one uppercase letter')

        if not any(char.islower() for char in v):
            raise ValueError(
                'Password should have at least one lowercase letter')

        return v
