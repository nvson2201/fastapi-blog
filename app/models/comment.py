from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .post import Post  # noqa: F401


class Comment(Base):

    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(255))

    contain_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    contain = relationship("Post", back_populates="comments")

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"{self.body}"
