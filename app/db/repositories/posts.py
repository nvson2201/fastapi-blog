from typing import List, Any, Optional

from sqlalchemy import desc

from app.db.repositories.base import BaseRepository
from app.models.posts import Post
from app.models import PostsToTags, Tag, Favorite, User
from app.schemas.posts import (
    PostCreate, PostUpdate,
    PostInDB, PostInDBCreate, PostInDBUpdate)
from app.config import settings
from app.db.repositories.tags import TagRepository
from app.models import FollowersToFollowings


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    _tag_repo: TagRepository

    def __init__(self, db):
        super().__init__(Post, db)
        self._tag_repo = TagRepository(db)

    def create(self, *, body: PostInDBCreate) -> Post:
        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        created_at = settings.current_time()

        create_data = PostInDB(
            views=0,
            created_at=created_at,
            updated_at=created_at,
            **body_dict
        )

        return super().create(body=create_data)

    def get_multi(
        self, *, author_id: int, offset: int = 0, limit: int = 100
    ) -> List[Post]:
        q = self.db.query(Post)
        q = q.filter(Post.author_id == author_id)
        q = q.limit(limit)
        q = q.offset(offset)

        posts = q.all()

        return posts

    def update(
        self,
        post: Post, *, body: PostInDBUpdate
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
        q = self.db.query(Post)
        q = q.filter(Post.id == id)
        post = q.first()
        post.views = Post.views + 1
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
            tags_list.append(tag.tag)

        return list(set(tags_list))

    def link_new_tags_to_post_by_id(self, *, id, tags: List[str]) -> None:

        tags = list(set(tags))
        self._tag_repo.create_tags_that_dont_exist(body=tags)
        for tag in tags:
            tag = self.db.query(Tag).filter(Tag.tag == tag).first()
            post_to_tag = PostsToTags(post_id=id, tag_id=tag.id)

            self.db.add(post_to_tag)
            self.db.commit()
            self.db.refresh(post_to_tag)

    def remove_link_tags_to_post_by_id(self, *, id, tags: List[str]) -> None:
        tags = list(set(tags))
        q = self.db.query(PostsToTags)
        q = q.filter(PostsToTags.post_id == id)
        q = q.where(PostsToTags.tag)
        q = q.filter(Tag.tag.in_(tags))
        q = q.delete(synchronize_session='fetch')
        self.db.commit()

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

        self.db.delete(favorite_record)
        self.db.commit()

    def get_posts_for_feed(
        self, *, user: User,
        limit: int = 20,
        offset: int = 0
    ) -> List[Post]:
        q = self.db.query(Post)
        q = q.join(
            FollowersToFollowings,
            FollowersToFollowings.following_id == Post.author_id
        )
        q = q.filter(FollowersToFollowings.follower_id == user.id)
        q = q.order_by(desc(Post.created_at))
        q = q.limit(limit)
        posts = q.offset(offset)

        return posts

    def posts_filters(
        self,
        *,
        tags: List[str] = None,
        author: Optional[str] = None,
        user_favorited: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        requested_user: Optional[User] = None,
    ) -> List[Post]:
        if tags:
            q = self.db.query(Post).distinct()
            q = q.where(Post.posts_to_tags)
            q = q.filter(PostsToTags.tag.has(Tag.tag.in_(tags)))

        if author:
            q = q.where(User.posts)
            q = q.filter(Post.author.has(User.username == author))

        if user_favorited:
            q = q.where(Post.favorites)
            q = q.filter(Favorite.user.has(
                User.username == user_favorited)
            )

        q = q.limit(limit)
        q = q.offset(offset)

        posts = q.all()

        return posts
