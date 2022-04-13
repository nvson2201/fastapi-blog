import email
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.schemas.post import Post


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True
