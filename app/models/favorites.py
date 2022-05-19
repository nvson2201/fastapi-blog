from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401
    from .posts import Post  # noqa: F401


class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), index=True)
    post = relationship("Post", back_populates="favorites")

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), index=True)
    user = relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"""
                    post_id: {self.post_id},
                    tag_id: {self.tag_id},
                """
