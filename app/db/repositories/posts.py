from typing import List, Any, Union, Dict


from app.db.repositories.base import BaseRepository
from app.models.posts import Post
from app.schemas.posts import PostCreate, PostUpdate, PostInDB
from app.config import settings
from app.db import db


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    def create_with_owner(
        self, *, body: PostCreate, author_id: int
    ) -> Post:
        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        created_at = settings.current_time()

        create_data = PostInDB(
            views=0,
            created_at=created_at,
            updated_at=created_at,
            author_id=author_id,
            **body_dict
        )

        return super().create(body=create_data)

    def get_multi_by_owner(
        self, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:

        q = self.db.query(self.model)
        q = q.filter(Post.author_id == author_id)
        q = q.limit(limit)
        q = q.offset(skip)

        posts = q.all()

        return posts

    def update(
        self,
        post: Post, *, body: Union[PostUpdate, Dict[str, Any]]
    ) -> Post:
        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        updated_at = settings.current_time()

        update_data = PostInDB(
            updated_at=updated_at,
            **body_dict
        )

        return super().update(post, body=update_data)

    def update_views(self, id: Any):
        q = self.db.query(self.model)
        q = q.filter(self.model.id == id)
        post = q.first()

        post.views = self.model.views + 1
        self.db.commit()
        self.db.refresh(post)

        return post


posts = PostRepository(Post, db)
