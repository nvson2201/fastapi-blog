from urllib import error

import click

from app.services.users import user_services
from app.services.posts import post_services
from app.db.repositories.tags import tags
from app.db.repositories.posts import posts


@click.command()
@click.option('--user_id', prompt='user_id')
def read_user_by_id(user_id):
    """
    Get a specific user by id.
    """
    user = user_services.get(id=user_id)
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
@click.option('--tags', prompt='tags', multiple=True, default=["chuoi", "qua"])
def add_tag_to_post_id(post_id, tags):
    posts.update_new_tags_to_post_by_id(id=post_id, tags=tags)


@click.command()
@click.option('--post_id', prompt='post_id')
def get_favorites_count_for_post_by_id(post_id):
    fav_counted = posts.get_favorites_count_for_post_by_id(id=post_id)
    print(fav_counted)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--user_id', prompt='user_id')
def is_post_favorited_by_user(post_id, user_id):
    user = user_services.get(user_id)
    post = post_services.get(post_id)
    is_right = posts.is_post_favorited_by_user(post=post, user=user)
    print(is_right)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--user_id', prompt='user_id')
def add_post_into_favorites(post_id, user_id):
    user1 = user_services.get(user_id)
    post_at_id = post_services.get(post_id)
    posts.add_post_into_favorites(post=post_at_id, user=user1)
    print(user1.id, post_at_id.id)


@click.command()
@click.option('--post_id', prompt='post_id')
@click.option('--user_id', prompt='user_id')
def delete_post_from_favorites(post_id, user_id):
    user1 = user_services.get(user_id)
    post_at_id = post_services.get(post_id)
    posts.delete_post_from_favorites(post=post_at_id, user=user1)
    print(user1.id, post_at_id.id)


if __name__ == '__main__':
    # read_user_by_id()
    # add_tags()
    # get_tags()
    # add_tag_to_post_id()
    # get_favorites_count_for_post_by_id()
    # is_post_favorited_by_user()
    # add_post_into_favorites()
    delete_post_from_favorites()
