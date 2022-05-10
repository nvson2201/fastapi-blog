from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class FollowersToFollowings(Base):

    __tablename__ = "followers_to_followings"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(255))

    follower_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True, index=True)
    follower = relationship("User", back_populates="following")

    following_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True, index=True)
    following = relationship("User", back_populates="follower")

    def __repr__(self):
        return f"""
                    post_id: {self.post_id},
                    tag_id: {self.tag_id},
                """
