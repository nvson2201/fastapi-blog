from typing import List

from fastapi.encoders import jsonable_encoder

from app.db.repositories.base import BaseRepository
from app.models.comments import Comment
from app.schemas.comments import CommentCreate, CommentUpdate


class CommentRepository(
        BaseRepository[Comment, CommentCreate, CommentUpdate]
):
    def __init__(self, db):
        super().__init__(Comment, db)

    def create_with_owner(
        self, *, body: CommentCreate,
        author_id: int, post_id: int
    ) -> Comment:
        body_dict = jsonable_encoder(body)
        comment = Comment(**body_dict, author_id=author_id,
                          post_id=post_id)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_multi_by_owner(
        self, *, author_id: int, post_id=int,
        offset: int = 0, limit: int = 100
    ) -> List[Comment]:

        q = self.db.query(Comment)
        q = q.filter(Comment.author_id == author_id,
                     Comment.post_id == post_id)
        q = q.limit(limit)
        q = q.offset(offset)

        comments = q.all()

        return comments
