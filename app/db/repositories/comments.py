from typing import List

from fastapi.encoders import jsonable_encoder

from app.db.repositories.base import BaseRepository
from app.models.comments import Comment
from app.schemas.comments import CommentCreate, CommentUpdate
from app.db import db


class CommentRepository(
        BaseRepository[Comment, CommentCreate, CommentUpdate]
):
    def create_with_owner(
        self, *, body: CommentCreate,
        author_id: int, post_id: int
    ) -> Comment:
        body_dict = jsonable_encoder(body)
        comment = self.model(**body_dict, author_id=author_id,
                             post_id=post_id)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_multi_by_owner(
        self, *, author_id: int, post_id=int,
        skip: int = 0, limit: int = 100
    ) -> List[Comment]:

        q = self.db.query(self.model)
        q = q.filter(Comment.author_id == author_id,
                     Comment.post_id == post_id)
        q = q.limit(limit)
        q = q.offset(skip)

        comments = q.all()

        return comments


comments = CommentRepository(Comment, db)
