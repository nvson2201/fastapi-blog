from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401
    from .posts import Post  # noqa: F401


class Notification(Base):

    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    post = relationship("Post", back_populates="notifications")

    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    sender = relationship("User", foreign_keys=[sender_id])

    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    receiver = relationship("User", foreign_keys=[receiver_id])

    def __repr__(self):
        return f"{self.body}"
