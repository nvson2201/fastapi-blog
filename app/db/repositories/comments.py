from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.models.comments import Comment
from app.schemas.comments import CommentCreate, CommentUpdate


class CommentRepository(BaseRepository[Comment, CommentCreate, CommentUpdate]):
    def create_with_owner(
        self, db: Session, *, body: CommentCreate,
        author_id: int, post_id: int
    ) -> Comment:
        body_dict = jsonable_encoder(body)
        comment = self.model(**body_dict, author_id=author_id,
                             post_id=post_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

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
