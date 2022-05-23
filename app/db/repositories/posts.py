from typing import List, Any, Union, Dict

from sqlalchemy import exc
from app.db.repositories.base import BaseRepository
from app.models.posts import Post
from app.models import PostsToTags, Tag, Favorite, User
from app.schemas.posts import PostCreate, PostUpdate, PostInDB
from app.config import settings
from app.db import db
from app.db.repositories.tags import TagRepository


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    def __init__(self, model, db):
        super().__init__(model, db)
        self._tag_repo = TagRepository(Tag, db)

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

    def get_tags_for_post_by_id(self, *, id) -> List[str]:
        q = self.db.query(PostsToTags)
        records = q.filter(PostsToTags.post_id == id)
        tag_ids = [item.tag_id for item in records]
        tags_list = []
        for tag_id in tag_ids:
            q = self.db.query(Tag)
            tag = q.filter(Tag.id == tag_id).first()
            tags_list.append(tag.id)

        return set(tags_list)

    def update_new_tags_to_post_by_id(self, *, id, tags: List[str]) -> None:
        self.db.query(PostsToTags).filter(
            PostsToTags.post_id == id).delete()
        self.db.commit()

        tags = self._tag_repo.create_tags_that_dont_exist(body=tags)
        for tag in tags:
            post_to_tag = PostsToTags(post_id=id, tag_id=tag.id)

            try:
                self.db.add(post_to_tag)
                self.db.commit()
            except exc.IntegrityError:
                raise Exception("No post with this id")

            self.db.refresh(post_to_tag)

    def get_favorites_count_for_post_by_id(
            self, *, id
    ) -> int:
        q = self.db.query(Favorite).filter(Favorite.post_id == id)
        favorites_count = q.count()
        return favorites_count

    def is_post_favorited_by_user(self, *, post: Post, user: User) -> bool:

        q = self.db.query(Favorite)
        q = q.filter(Favorite.post_id == post.id)

        favorite_record = q.filter(Favorite.user_id == user.id).first()

        if favorite_record:
            return True
        else:
            return False

    def add_post_into_favorites(self, *, post: Post, user: User) -> None:

        if self.is_post_favorited_by_user(post=post, user=user):
            raise Exception('Already favorited!')

        favorite_record = Favorite()

        favorite_record.post_id = post.id
        favorite_record.user_id = user.id

        self.db.add(favorite_record)
        self.db.commit()
        self.db.refresh(favorite_record)

    def delete_post_from_favorites(self, *, post: Post, user: User) -> None:

        q = self.db.query(Favorite)
        q = q.filter(Favorite.post_id == post.id)

        favorite_record = q.filter(Favorite.user_id == user.id).first()

        if not favorite_record:
            raise Exception('Not favorited yet!')

        self.db.delete(favorite_record)
        self.db.commit()


posts = PostRepository(Post, db)
