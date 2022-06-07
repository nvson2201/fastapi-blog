from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.plugins.mysql.base_class import Base

if TYPE_CHECKING:
    from .users import User  # noqa: F401


class Code(Base):
    __tablename__ = "codes"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(255))
    fails = Column(Integer)
    time_lock_send_code = Column(DateTime)
    time_lock_fail = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="code")

    def __repr__(self):
        return f"""     id: {self.id},
                        body: {self.body},
                        fails: {self.fails},
                        time_lock_send_code: {self.time_lock_send_code},
                        time_lock_fail: {self.time_lock_fail},
                        user_id: {self.user_id}
                    """
