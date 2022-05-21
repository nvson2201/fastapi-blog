from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[int] = None


class PostCreate(PostBase):
    title: str
    body: str


class PostUpdate(PostBase):
    pass


class PostUpdateView(BaseModel):
    id: int
    views: Optional[int] = None


class PostInDBBase(PostBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    views: Optional[int] = None

    class Config:
        orm_mode = True


class Post(PostInDBBase):  # response_model
    pass


class PostInDB(PostInDBBase):
    pass
