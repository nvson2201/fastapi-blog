from typing import List

from sqlalchemy import exc

from app.models.posts import Post
from app.schemas.posts import PostUpdate, PostCreate
from app.exceptions.posts import PostNotFound, PostDuplicate
from app.db.repositories_cache.posts import PostRedisRepository
from app.plugins.kafka import producer
from app.db import repositories_cache


class PostServices:

    def __init__(self, repository: PostRedisRepository):
        self.repository = repository

    def get(self, id: str):
        post = self.repository.get(id)
        if not post:
            raise PostNotFound

        producer.produce({'id': post.id})

        return post

    def update(self, id: str, body: PostUpdate):
        post = self.repository.get(id)

        if not post:
            raise PostNotFound

        try:
            post = self.repository.update(self.post, body=body)
        except exc.IntegrityError:
            raise PostDuplicate

        return post

    def create_with_owner(self, body: PostCreate, author_id: int):

        post = self.repository.create_with_owner(
            body=body, author_id=author_id)

        return post

    def get_multi_by_owner(
        self, author_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Post]:

        posts = self.repository.get_multi_by_owner(
            author_id=author_id,
            skip=skip, limit=limit,
        )

        return posts

    def remove(self, id: int):
        return self.repository.remove(id)

    def update_views(self, id: int):
        self.repository.update_views(id)


post_services = PostServices(repository=repositories_cache.posts)
