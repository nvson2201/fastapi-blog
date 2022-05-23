from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field
from app.schemas.profiles import Profile


class PostBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    author: Optional[Profile] = None
    tags: Optional[List[str]] = None
    favorited: Optional[bool] = None
    favorites_count: Optional[int] = None


class PostInResponse(PostBase):  # response_model
    tags: Optional[List[str]] = Field(..., alias="tagList")


class ListOfPostsInResponse(BaseModel):
    posts: Optional[List[PostInResponse]] = None
    posts_count: Optional[int] = None


class PostCreate(BaseModel):
    title: str
    body: str
    tags: Optional[List[str]] = Field([], alias="tagList")


class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


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
    tags: List[str] = Field(..., alias="tagList")


class PostInDB(PostInDBBase):
    pass
