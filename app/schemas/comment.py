from typing import Optional

from pydantic import BaseModel


# Shared properties
class CommentBase(BaseModel):
    body: Optional[str] = None


# Properties to receive on comment creation
class CommentCreate(CommentBase):
    body: str


# Properties to receive on comment update
class CommentUpdate(CommentBase):
    pass


# Properties shared by models stored in DB
class CommentInDBBase(CommentBase):
    id: int
    body: str
    owner_id: int
    contain_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Comment(CommentInDBBase):
    pass


# Properties properties stored in DB
class CommentInDB(CommentInDBBase):
    pass
