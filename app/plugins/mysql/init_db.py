from sqlalchemy.orm import Session
from app import schemas

from app.db.repositories.users import UserRepository
from app.db.repositories.posts import PostRepository
from app.db.repositories.comments import CommentRepository
from app.plugins.mysql import base  # noqa: F401
from app.config import settings
import random


def init_db(db: Session) -> None:
    users = UserRepository(db)
    posts = PostRepository(db)
    comments = CommentRepository(db)

    def get_random_number():
        return random.choice([i for i in range(1, 11)])

    def get_tags():
        array_tag = ["animal", "people", "game", "house", "moon", "ring"]
        return list(set(random.choices(
            array_tag,
            k=random.choice([1, 2, 3])
        )))

    user1 = users.get_by_email(email=settings.FIRST_SUPERUSER)
    if not user1:
        first_superuser = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username=settings.FIRST_SUPERUSER_USERNAME,
            is_superuser=True,
        )
        user1 = users.create(body=first_superuser)
    # Create 10 users:
    arr_users = [user1]
    for i in range(2, 11):
        email = f"user{str(i)}@gmail.com"
        password = "123456aA"
        username = "user{}".format(i)
        user = schemas.UserCreate(
            email=email,
            password=password,
            username=username,
        )
        new_user = users.create(body=user)
        arr_users.append(new_user)

    # Create 10 row followers:
    for i in range(1, 11):
        user1 = random.choice(arr_users)
        for i in range(random.choice([i for i in range(1, 4)])):
            user2 = random.choice(arr_users)
            users.add_user_into_followers(
                target_user=user1,
                requested_user=user2
            )

    # Create 10 posts:
    arr_posts = []
    for i in range(1, 11):
        title = "post {}".format(i)
        body = "This is a post {}".format(i)

        post = schemas.PostInDBCreate(
            title=title,
            body=body,
            author_id=get_random_number()
        )
        post = posts.create(body=post)

        posts.link_new_tags_to_post_by_id(
            id=post.id,
            tags=get_tags()
        )
        arr_posts.append(post)

    # Create 10 comments:
    for i in range(1, 11):

        comment = schemas.CommentCreate(
            body="This is a comment {}".format(i)
        )

        comments.create_with_owner(
            body=comment,
            author_id=get_random_number(),
            post_id=get_random_number()
        )

        # Create 10 row favorites:
        posts.add_post_into_favorites(
            post=random.choice(arr_posts),
            user=random.choice(arr_users)
        )
