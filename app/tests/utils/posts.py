from typing import Optional
from app.db.repositories.posts import PostRepository

from app.models import Post
from app.schemas.posts import PostInDBCreate
from app.db.repositories.users import UserRepository
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_post(
        user_repo: UserRepository, post_repo: PostRepository, *,
        author_id: Optional[int] = None
) -> Post:

    if author_id is None:
        user = create_random_user(user_repo)
        author_id = user.id
    title = random_lower_string()
    body = random_lower_string()
    post_body = PostInDBCreate(
        title=title,
        body=body,
        author_id=author_id)
    return post_repo.create(body=post_body)
