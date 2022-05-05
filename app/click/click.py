from urllib import error

import click

from app.api import deps
from app.services.crud_cache import UserServices

db = next(deps.get_db())
user_services = UserServices(db)


@click.command()
@click.option('--user_id', prompt='user_id')
def read_user_by_id(user_id):
    """
    Get a specific user by id.
    """
    user = user_services.get_by_id(db, id=user_id)
    if not user:
        raise error.HTTPError(
            code=404, msg="User not found", url=None,
            hdrs=None, fp=None)

    print(user)


if __name__ == '__main__':
    read_user_by_id()
