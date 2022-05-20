from typing import List, Any

from fastapi.encoders import jsonable_encoder

from app.db.repositories.base import BaseRepository
from app.models.posts import Post
from app.schemas.posts import PostCreate, PostUpdate
from app.db import db


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    def create_with_owner(
        self, *, body: PostCreate, author_id: int
    ) -> Post:
        body_dict = jsonable_encoder(body)
        post = self.model(**body_dict, author_id=author_id)
        post.views = 0
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        return post

    def get_multi_by_owner(
        self, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:

        q = self.db.query(self.model)
        q = q.filter(Post.author_id == author_id)
        q = q.limit(limit)
        q = q.offset(skip)

        posts = q.all()

        return posts

    def update_views(self, id: Any):
        q = self.db.query(self.model)
        q = q.filter(self.model.id == id)
        post = q.first()

        post.views = self.model.views + 1
        self.db.commit()
        self.db.refresh(post)

        return post


posts = PostRepository(Post, db)
