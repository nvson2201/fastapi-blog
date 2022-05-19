from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401
    from .comments import Comment  # noqa: F401
    from .posts_to_tags import PostsToTags  # noqa: F401
    from .favorites import Favorite  # noqa: F401


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    views = Column(Integer)
    title = Column(String(50))
    body = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="posts")

    comments = relationship(
        "Comment", back_populates="post", cascade="all,delete")

    posts_to_tags = relationship(
        "PostsToTags", back_populates="post", cascade="all,delete")

    favorites = relationship(
        "Favorite", back_populates="post", cascade="all,delete")

    def __repr__(self):
        return f"{self.title}"
