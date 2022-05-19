from typing import List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.models.posts import Post
from app.schemas.posts import PostCreate, PostUpdate


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    def create_with_owner(
        self, db: Session, *, body: PostCreate, author_id: int
    ) -> Post:
        body_dict = jsonable_encoder(body)
        post = self.model(**body_dict, author_id=author_id)
        post.views = 0
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

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

    def update_views(self, db: Session, id: Any):
        post = db.query(self.model).filter(self.model.id == id).first()
        post.views = self.model.views + 1
        db.commit()
        db.refresh(post)

        return post


posts = PostRepository(Post)
