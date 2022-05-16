from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .post import Post  # noqa: F401


class Comment(Base):

    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(255))

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    post = relationship("Post", back_populates="comments")

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"{self.body}"
