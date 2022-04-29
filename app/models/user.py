from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column((String(50)), index=True)
    email = Column((String(255)), unique=True, index=True, nullable=False)
    hashed_password = Column((String(225)), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)
    posts = relationship(
        "Post", back_populates="owner", cascade="all,delete")
    comments = relationship(
        "Comment", back_populates="owner", cascade="all,delete")

    def __repr__(self):
        return f"{self.email}"
