from typing import List, Union

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostUpdate, PostCreate
from app.exceptions.posts import PostNotFound, PostDuplicate
from app.db.repositories_cache.posts import PostRedisRepository
from app.db.repositories.posts import PostRepository


class PostServices:

    def __init__(self, db: Session,
                 crud_engine: Union[PostRedisRepository, PostRepository]):
        self.db = db
        self.crud_engine = crud_engine

    def get_by_id(self, id: str):
        post = self.crud_engine.get(self.db, id=id)
        if not post:
            raise PostNotFound

        return post

    def update_by_id(self, id: str, body: PostUpdate):
        post = self.crud_engine.get(self.db, id=id)

        if not post:
            raise PostNotFound

        try:
            post = self.crud_engine.update(
                self.db, db_obj=post, obj_in=body)
        except exc.IntegrityError:
            raise PostDuplicate

        return post

    def create_with_owner(self, body: PostCreate, author_id: int):

        post = self.crud_engine.create_with_owner(
            self.db, obj_in=body, author_id=author_id)

        return post

    def get_multi_by_owner(
        self, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        posts = self.crud_engine.get_multi_by_owner(
            self.db, author_id=author_id,
            skip=skip, limit=limit,
        )

        return posts

    def remove(self, db: Session, id: int):
        return self.crud_engine.remove(db, id=id)
