from app.db import repositories
from typing import List, Union

from sqlalchemy import exc

from app.models.posts import Post
from app.schemas.posts import PostUpdate, PostCreate
from app.exceptions.posts import PostNotFound, PostDuplicate
from app.db.repositories_cache.posts import PostRedisRepository
from app.db.repositories.posts import PostRepository
from app.plugins.kafka import producer
from app.db import repositories_cache


class PostServices:

    def __init__(self,
                 crud_engine: Union[PostRedisRepository, PostRepository]):
        self.crud_engine = crud_engine

    def get(self, id: str):
        post = self.crud_engine.get(id)
        if not post:
            raise PostNotFound

        producer.produce({'id': post.id})

        return post

    def update(self, id: str, body: PostUpdate):
        post = self.crud_engine.get(id)

        if not post:
            raise PostNotFound

        try:
            post = self.crud_engine.update(self.post, body=body)
        except exc.IntegrityError:
            raise PostDuplicate

        return post

    def create_with_owner(self, body: PostCreate, author_id: int):

        post = self.crud_engine.create_with_owner(
            body=body, author_id=author_id)

        return post

    def get_multi_by_owner(
        self, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        posts = self.crud_engine.get_multi_by_owner(
            author_id=author_id,
            skip=skip, limit=limit,
        )

        return posts

    def remove(self, id: int):
        return self.crud_engine.remove(id)

    def update_views(self, id: int):
        self.crud_engine.update_views(id)


post_services = PostServices(crud_engine=repositories.users)
post_redis_services = PostServices(crud_engine=repositories_cache.posts)
