from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentRepository(BaseRepository[Comment, CommentCreate, CommentUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CommentCreate,
        author_id: int, post_id: int
    ) -> Comment:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id,
                            post_id=post_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, author_id: int, post_id=int,
        skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.author_id == author_id,
                    Comment.post_id == post_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


comments = CommentRepository(Comment)
