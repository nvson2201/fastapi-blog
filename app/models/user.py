from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.config import settings
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column((String(50)), index=True)
    email = Column((String(255)), unique=True, index=True, nullable=False)
    hashed_password = Column((String(225)), nullable=False)
    created_date = Column(DateTime, default=settings.LOCAL_CURRENT_TIME)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_banned = Column(Boolean(), default=False)

    posts = relationship(
        "Post", back_populates="owner", cascade="all,delete")
    comments = relationship(
        "Comment", back_populates="owner", cascade="all,delete")

    def __repr__(self):
        return f"""
                    fullname: {self.full_name},
                    email: {self.email},
                    passowrd: {self.hashed_password},
                    is_active: {self.is_active},
                    is_superuser: {self.is_superuser}
                """
