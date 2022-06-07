from sqlalchemy.orm import Session
from app import schemas

from app.db.repositories.users import UserRepository
from app.db.repositories.posts import PostRepository
from app.db.repositories.comments import CommentRepository
from app.models.followers_to_followings import FollowersToFollowings
from app.plugins.mysql import base  # noqa: F401
from app.config import settings
import random

from app.utils.security import get_password_hash


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

    first_superuser = schemas.UserInDB(
        created_at=settings.current_time(),
        updated_at=settings.current_time(),
        email=settings.FIRST_SUPERUSER,
        hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
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
        user = schemas.UserInDB(
            created_at=settings.current_time(),
            updated_at=settings.current_time(),
            email=email,
            hashed_password=get_password_hash(password),
            username=username,
        )
        new_user = users.create(body=user)
        arr_users.append(new_user)

    # Create 10 row followers:
    for i in range(1, 11):
        user1 = random.choice(arr_users)
        for i in range(random.choice([i for i in range(1, 4)])):
            user2 = random.choice(arr_users)
            users.add_follower_to_following(
                follower_to_following=FollowersToFollowings(
                    follower_id=user2.id,
                    following_id=user1.id
                )
            )

    # Create 10 posts:
    arr_posts = []
    for i in range(1, 11):
        title = "post {}".format(i)
        body = "This is a post {}".format(i)

        post = schemas.PostInDB(
            title=title,
            body=body,
            author_id=get_random_number(),
            views=0
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
