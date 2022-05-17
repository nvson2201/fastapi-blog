from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.plugins.mysql.base_class import Base


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column((String(50)), index=True)

    posts_to_tags = relationship(
        "PostsToTags", back_populates="tag", cascade="all,delete")

    def __repr__(self):
        return f"""
                    tag: {self.tag},
                """
