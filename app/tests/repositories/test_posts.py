from app.models import User
from app.schemas.posts import PostInDBCreate, PostUpdate

from app.db.repositories.posts import PostRepository
from app.tests.utils.utils import random_lower_string


class TestPostRepository:

    def test_create_post(
        self,
        random_user: User,
        post_repo: PostRepository
    ) -> None:
        title = random_lower_string()
        body = random_lower_string()
        user = random_user
        post_body = PostInDBCreate(
            title=title,
            body=body,
            author_id=user.id)
        post = post_repo.create(body=post_body)

        assert post.title == title
        assert post.body == body
        assert post.author_id == user.id

    def test_get_post(
        self,
        random_user: User,
        post_repo: PostRepository
    ) -> None:
        title = random_lower_string()
        body = random_lower_string()
        user = random_user
        post_body = PostInDBCreate(
            title=title,
            body=body,
            author_id=user.id)
        post = post_repo.create(body=post_body)
        stored_post = post_repo.get(id=post.id)
        assert stored_post
        assert post.id == stored_post.id
        assert post.title == stored_post.title
        assert post.body == stored_post.body
        assert post.author_id == stored_post.author_id

    def test_update_post(self, random_user: User,
                         post_repo: PostRepository) -> None:
        title = random_lower_string()
        body = random_lower_string()
        user = random_user
        post_body = PostInDBCreate(
            title=title,
            body=body,
            author_id=user.id)
        post = post_repo.create(body=post_body)

        body2 = random_lower_string()
        post_update = PostUpdate(body=body2)
        post2 = post_repo.update(post, body=post_update)
        assert post.id == post2.id
        assert post.title == post2.title
        assert post2.body == body2
        assert post.author_id == post2.author_id

    def test_delete_post(self, random_user: User,
                         post_repo: PostRepository) -> None:
        title = random_lower_string()
        body = random_lower_string()
        user = random_user
        post_body = PostInDBCreate(
            title=title,
            body=body,
            author_id=user.id)
        post = post_repo.create(body=post_body)
        post2 = post_repo.remove(id=post.id)
        post3 = post_repo.get(id=post.id)
        assert post3 is None
        assert post2.id == post.id
        assert post2.title == title
        assert post2.body == body
        assert post2.author_id == user.id
