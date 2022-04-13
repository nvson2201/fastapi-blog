from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .post import Post  # noqa: F401


class Comment(Base):

    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(255))

    contain_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    contain = relationship("Post", back_populates="comment")

    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="comment")

    def __repr__(self):
        return f"{self.body}"
