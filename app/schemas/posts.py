from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field
from app.schemas.profiles import Profile
from app.schemas.common import DateTimeModelMixin


class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = Field([], alias="tagList")


class ListOfPostsInResponse(BaseModel):
    posts: Optional[List[PostInResponse]] = None
    posts_count: Optional[int] = None


class PostCreate(BaseModel):
    title: str
    body: str
    tags: Optional[List[str]] = Field([], alias="tagList")


class PostInResponse(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    author: Optional[Profile] = None
    tags: Optional[List[str]] = Field(..., alias="tagList")
    favorited: Optional[bool] = None
    favorites_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    views: Optional[int] = None


class ListOfPostsInResponse(BaseModel):
    posts: Optional[List[PostInResponse]] = None
    posts_count: Optional[int] = None


class PostInDBCreate(BaseModel):
    title: str
    body: str
    author_id: int


class PostInDB(DateTimeModelMixin):
    title: str
    body: str
    author_id: int
    views: int


class PostUpdateView(BaseModel):
    id: int
    views: Optional[int] = None

    class Config:
        orm_mode = True


