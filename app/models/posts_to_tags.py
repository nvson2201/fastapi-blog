from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .tag import Tag  # noqa: F401
    from .post import Post  # noqa: F401


class PostsToTags(Base):

    __tablename__ = "posts_to_tags"

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True, index=True)
    post = relationship("Post", back_populates="posts_to_tags")

    tag_id = Column(Integer, ForeignKey(
        "tags.id", ondelete="CASCADE"), primary_key=True, index=True)
    tag = relationship("Tag", back_populates="posts_to_tags")

    def __repr__(self):
        return f"""
                    post_id: {self.post_id},
                    tag_id: {self.tag_id},
                """
