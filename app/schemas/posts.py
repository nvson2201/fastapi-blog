from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field
from app.schemas.profiles import Profile
from app.config import settings


class PostCreate(BaseModel):
    title: str
    body: str
    tags: Optional[List[str]] = Field([], alias="tagList")


class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = Field([], alias="tagList")

class PostInDBCreate(BaseModel):
    title: str
    body: str
    author_id: int


class PostInDBUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class PostInDB(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    views: Optional[int] = None


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


class PostsFilters(BaseModel):
    tags: Optional[str] = None
    author: Optional[str] = None
    user_favorited: Optional[str] = None
    limit: int = Field(settings.DEFAULT_ARTICLES_LIMIT, ge=1)
    offset: int = Field(settings.DEFAULT_ARTICLES_OFFSET, ge=0)


class PostUpdateView(BaseModel):
    id: int
    views: Optional[int] = None

    class Config:
        orm_mode = True


