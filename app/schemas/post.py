import email
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    body: Optional[str] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner: EmailStr

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str]
    body: Optional[str]

    class Config:
        orm_mode = True
