from sqlalchemy.orm import Session

from app.db.repositories import posts
from app.schemas.posts import PostCreate, PostUpdate
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_post(db: Session) -> None:
    title = random_lower_string()
    body = random_lower_string()
    post_body = PostCreate(title=title, body=body)
    user = create_random_user(db)
    post = posts.create_with_owner(
        body=post_body, author_id=user.id)
    assert post.title == title
    assert post.body == body
    assert post.author_id == user.id


def test_get_post(db: Session) -> None:
    title = random_lower_string()
    body = random_lower_string()
    post_body = PostCreate(title=title, body=body)
    user = create_random_user(db)
    post = posts.create_with_owner(
        body=post_body, author_id=user.id)
    stored_post = posts.get(id=post.id)
    assert stored_post
    assert post.id == stored_post.id
    assert post.title == stored_post.title
    assert post.body == stored_post.body
    assert post.author_id == stored_post.author_id


def test_update_post(db: Session) -> None:
    title = random_lower_string()
    body = random_lower_string()
    post_body = PostCreate(title=title, body=body)
    user = create_random_user(db)
    post = posts.create_with_owner(
        body=post_body, author_id=user.id)
    body2 = random_lower_string()
    post_update = PostUpdate(body=body2)
    post2 = posts.update(post, body=post_update)
    assert post.id == post2.id
    assert post.title == post2.title
    assert post2.body == body2
    assert post.author_id == post2.author_id


def test_delete_post(db: Session) -> None:
    title = random_lower_string()
    body = random_lower_string()
    post_body = PostCreate(title=title, body=body)
    user = create_random_user(db)
    post = posts.create_with_owner(
        body=post_body, author_id=user.id)
    post2 = posts.remove(id=post.id)
    post3 = posts.get(id=post.id)
    assert post3 is None
    assert post2.id == post.id
    assert post2.title == title
    assert post2.body == body
    assert post2.author_id == user.id
