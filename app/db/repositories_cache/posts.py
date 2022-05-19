from typing import Any, Dict, Union, List, Optional

from sqlalchemy.orm import Session

from app.models.posts import Post
from app.schemas.posts import PostUpdate, PostCreate
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator


class PostRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def get(self, db: Session, id: Any) -> Optional[Post]:
        cache_data = self._get_cache(id)

        if cache_data:
            post = Post(**cache_data)
        else:
            post = self.crud_component.get(db, id)
            if post:
                self._set_cache(id, data=post)

        return post

    def create_with_owner(self, db: Session,
                          body: PostCreate, author_id: int):
        post = self.crud_component.create_with_owner(
            db, body=body, author_id=author_id)

        self._set_cache(id=post.id, data=post)

        return post

    def update(
        self, db: Session,
        post: Post,  *, body: Union[PostUpdate, Dict[str, Any]]
    ) -> Post:
        post = self.crud_component.update(db, post, body=body)
        self._set_cache(id=post.id, data=post)

        return post

    def get_multi_by_owner(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        return self.crud_component.get_multi_by_owner(
            db, author_id=author_id, skip=skip, limit=limit,
        )

    def remove(self, db: Session, id: Any):
        return self.crud_component.remove(db, id)
