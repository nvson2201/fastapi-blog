from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    body: Optional[str] = None


class CommentCreate(CommentBase):
    body: str


class CommentUpdate(CommentBase):
    pass


class CommentInDBBase(CommentBase):
    id: int
    body: str
    owner_id: int
    contain_id: int

    class Config:
        orm_mode = True


class Comment(CommentInDBBase):
    pass


class CommentInDB(CommentInDBBase):
    pass
