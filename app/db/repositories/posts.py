from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PostCreate, author_id: int
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        return (
            db.query(self.model)
            .filter(Post.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


posts = PostRepository(Post)
