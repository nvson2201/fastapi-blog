from typing import List, Any, Optional

from sqlalchemy import desc

from app.db.repositories.base import BaseRepository
from app.models.posts import Post
from app.models import PostsToTags, Tag, Favorite, User
from app.schemas.posts import PostCreate, PostUpdate
from app.db.repositories.tags import TagRepository
from app.models import FollowersToFollowings


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    _tag_repo: TagRepository

    def __init__(self, db):
        super().__init__(Post, db)
        self._tag_repo = TagRepository(db)

    def get_multi(
        self, *, author_id: int, offset: int = 0, limit: int = 100
    ) -> List[Post]:
        q = self.db.query(Post)
        q = q.filter(Post.author_id == author_id)
        q = q.limit(limit)
        q = q.offset(offset)

        posts = q.all()

        return posts

    def update_views(self, id: Any):
        post = self.db.query(Post).filter(Post.id == id).first()
        post.views = Post.views + 1
        self.db.commit()
        self.db.refresh(post)

        return post

    def get_tags_for_post_by_id(self, *, id) -> List[str]:
        post_to_tags = self.db.query(PostsToTags).filter(
            PostsToTags.post_id == id)
        tag_ids = [item.tag_id for item in post_to_tags]
        tags_list = []

        for tag_id in tag_ids:
            tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
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

    def get_favorites_count_for_post_by_id(self, *, id) -> int:
        return self.db.query(Favorite).filter(
            Favorite.post_id == id).count()

    def is_post_favorited_by_user(self, *, post: Post, user: User) -> bool:
        favorite = self.db.query(Favorite).filter(
            Favorite.post_id == post.id,
            Favorite.user_id == user.id
        ).first()

        return bool(favorite)

    def add_post_into_favorites(self, *, post: Post, user: User) -> None:
        favorite_record = Favorite(
            post_id=post.id,
            user_id=user.id
        )

        self.db.add(favorite_record)
        self.db.commit()
        self.db.refresh(favorite_record)

    def delete_post_from_favorites(self, *, post: Post, user: User) -> None:
        favorite = self.db.query(Favorite).filter(
            Favorite.post_id == post.id,
            Favorite.user_id == user.id
        ).first()

        self.db.delete(favorite)
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
    ) -> List[Post]:
        q = self.db.query(Post)
        if tags:
            q.distinct().where(Post.posts_to_tags) \
                .filter(PostsToTags.tag.has(Tag.tag.in_(tags)))

        if author:
            q = q.where(User.posts).filter(
                Post.author.has(User.username == author))

        if user_favorited:
            q = q.where(Post.favorites).filter(Favorite.user.has(
                User.username == user_favorited)
            )

        q = q.limit(limit).offset(offset)

        return q.all()
