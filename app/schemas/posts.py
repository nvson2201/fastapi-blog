from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class PostCreate(PostBase):
    title: str
    body: str


class PostUpdate(PostBase):
    pass


class PostUpdateView(BaseModel):
    id: int
    views: Optional[int] = None


class PostInDBBase(PostBase):
    id: int
    title: str
    body: str
    author_id: int
    views: int

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass


class PostInDB(PostInDBBase):
    pass
