from typing import Optional

from sqlalchemy.orm import Session

from app import models
from app.schemas.posts import PostCreate
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_lower_string
from app.db.repositories import posts


def create_random_post(db: Session, *,
                       author_id: Optional[int] = None) -> models.Post:
    if author_id is None:
        user = create_random_user(db)
        author_id = user.id
    title = random_lower_string()
    body = random_lower_string()
    post_body = PostCreate(title=title, body=body)
    return posts.create_with_owner(
        body=post_body, author_id=author_id)
