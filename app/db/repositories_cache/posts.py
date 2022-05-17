from typing import Any, Dict, Union, List, Optional

from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostUpdate, PostCreate
from app.decorators.component import (
    ModelType, CreateSchemaType, UpdateSchemaType)
from app.db.repositories_cache.base import RedisDecorator


class PostRedisRepository(
    RedisDecorator[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def get(self, db: Session, id: Any) -> Optional[Post]:
        cache_data = self._get_cache(id=id)

        if cache_data:
            post = Post(**cache_data)
        else:
            post = self.crud_component.get(db=db, id=id)
            if post:
                self._set_cache(id=id, data=post)

        return post

    def create_with_owner(self, db: Session,
                          obj_in: PostCreate, author_id: int):
        post = self.crud_component.create_with_owner(
            db, obj_in=obj_in, author_id=author_id)

        self._set_cache(id=post.id, data=post)

        return post

    def update(
        self, db: Session, *,
        db_obj: Post, obj_in: Union[PostUpdate, Dict[str, Any]]
    ) -> Post:
        post = self.crud_component.update(db, db_obj=db_obj, obj_in=obj_in)
        self._set_cache(id=post.id, data=post)

        return post

    def get_multi_by_owner(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        return self.crud_component.get_multi_by_owner(
            db, author_id=author_id, skip=skip, limit=limit,
        )

    def remove(self, db: Session, id: Any):
        return self.crud_component.remove(db, id=id)
