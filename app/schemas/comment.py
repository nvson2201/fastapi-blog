import email
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class CommentBase(BaseModel):
    body: Optional[str] = None


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    owner: EmailStr
    contain: int

    class Config:
        orm_mode = True


class CommentUpdate(BaseModel):
    body: Optional[str]

    class Config:
        orm_mode = True
