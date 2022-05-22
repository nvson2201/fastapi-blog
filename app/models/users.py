from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .posts import Post  # noqa: F401
    from .comments import Comment  # noqa: F401
    from .favorites import Favorite  # noqa: F401
    from .followers_to_followings import FollowersToFollowings  # noqa: F401


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column((String(50)), index=True)
    email = Column((String(255)), unique=True, index=True, nullable=False)
    username = Column((String(255)), unique=True, index=True, nullable=False)
    hashed_password = Column((String(225)), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_banned = Column(Boolean(), default=False)

    posts = relationship(
        "Post", back_populates="author", cascade="all,delete")
    comments = relationship(
        "Comment", back_populates="author", cascade="all,delete")
    favorites = relationship(
        "Favorite", back_populates="user", cascade="all,delete")
    # follower = relationship(
    #     "FollowersToFollowings",
    #     back_populates="following", cascade="all,delete")
    # following = relationship(
    #     "FollowersToFollowings",
    #     back_populates="follower", cascade="all,delete")


def __repr__(self):
    return f"""
                    fullname: {self.full_name},
                    email: {self.email},
                    passowrd: {self.hashed_password},
                    is_active: {self.is_active},
                    is_superuser: {self.is_superuser}
                """
