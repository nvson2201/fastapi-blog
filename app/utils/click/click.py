from urllib import error

import click

from app.db.repositories.tags import TagRepository

from app.db.repositories.users import UserRepository
from app.db.repositories.posts import PostRepository
from app.schemas.posts import PostUpdate
from app.db.db import get_db

db = next(get_db())
users = UserRepository(db)
posts = PostRepository(db)
tags = TagRepository(db)


@click.command()
@click.option('--user_id', prompt='user_id')
def read_user_by_id(user_id):
    """
    Get a specific user by id.
    """
    user = users.get(id=user_id)
    if not user:
        raise error.HTTPError(
            code=404, msg="User not found", url=None,
            hdrs=None, fp=None)

    print(user)


@click.command()
@click.option('--body', prompt='tag', multiple=True, default=["hoa", "qua"])
def add_tags(body):
    """
    Get a specific user by id.
    """
    tagsList = tags.create_tags_that_dont_exist(body=body)
    if not tagsList:
        raise error.HTTPError(
            code=404, msg="Not found", url=None,
            hdrs=None, fp=None)

    print(tagsList)


@click.command()
@click.option('--user_id', prompt='user_id')
def get_tags(user_id):
    """
    Get a specific user by id.
    """
    tagsList = tags.get_all_tags()
    if not tagsList:
        raise error.HTTPError(
            code=404, msg="Not found", url=None,
            hdrs=None, fp=None)

    print(user_id, tagsList)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--tags', prompt='tags', multiple=True, default=["cam", "quyt"])
def link_new_tags_to_post_by_id(post_id, tags):
    posts.link_new_tags_to_post_by_id(id=post_id, tags=tags)


@click.command()
@click.option('--post_id', prompt='post_id')
def get_favorites_count_for_post_by_id(post_id):
    fav_counted = posts.get_favorites_count_for_post_by_id(id=post_id)
    print(fav_counted)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--user_id', prompt='user_id')
def is_post_favorited_by_user(post_id, user_id):
    user = users.get(user_id)
    post = posts.get(post_id)
    is_right = posts.is_post_favorited_by_user(post=post, user=user)
    print(is_right)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--user_id', prompt='user_id')
def add_post_into_favorites(post_id, user_id):
    user1 = users.get(user_id)
    post_at_id = posts.get(post_id)
    posts.add_post_into_favorites(post=post_at_id, user=user1)
    print(user1.id, post_at_id.id)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--user_id', prompt='user_id')
def delete_post_from_favorites(post_id, user_id):
    user1 = users.get(user_id)
    post_at_id = posts.get(post_id)
    posts.delete_post_from_favorites(post=post_at_id, user=user1)
    print(user1.id, post_at_id.id)


@click.command()
@click.option('--post_id', prompt='post_id')
def get_tags_for_post_by_id(post_id):
    tags = posts.get_tags_for_post_by_id(id=post_id)
    print(tags)


@click.command()
@click.option('--user_favorited', prompt='user favorited')
@click.option('--author', prompt='author name')
@click.option('--tags', prompt='tags',
              multiple=True, default=["dong vat"])
def posts_filters(author, tags, user_favorited):
    posts.posts_filters(
        tags=tags, author=author,
        user_favorited=user_favorited,
    )


@click.command()
@click.option('--post_id', prompt='post_id')
def update_post(post_id):

    body = PostUpdate(
        title="hoa hong",
        body="hoa hong dep",
        tagList=["thuc vat"]
    )
    post_in_db_after_update = posts.update(id=post_id, body=body)
    print(post_in_db_after_update.title, post_in_db_after_update.body)


@click.command()
@click.option('--post_id', prompt='post_id')
def remove_link_tags_to_post_by_id(post_id):
    tags = ["hoa qua"]
    posts.remove_link_tags_to_post_by_id(id=post_id, tags=tags)


@click.command()
@click.option('--user_id', prompt='user_id')
def get_all_followers(user_id):
    users.get_all_followers(user_id)


if __name__ == '__main__':
    # read_user_by_id()
    # add_tags()
    # get_tags()
    # link_new_tags_to_post_by_id()
    # get_favorites_count_for_post_by_id()
    # is_post_favorited_by_user()
    # add_post_into_favorites()
    # delete_post_from_favorites()
    # get_tags_for_post_by_id()
    # posts_filters()
    # update_post()
    # remove_link_tags_to_post_by_id()
    get_all_followers()
