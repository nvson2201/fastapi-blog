from urllib import error

import click

from app.api import deps
from app.services.crud_cache import UserServices
from app.decorators.crud.redis_decorator.user import CRUDRedisUserDecorator
from app.config import settings
from app import crud

db = next(deps.get_db())

user_redis_decorator = CRUDRedisUserDecorator(
    crud.user, settings.REDIS_SUFFIX_USER
)

user_services = UserServices(db, user_redis_decorator)


@click.command()
@click.option('--user_id', prompt='user_id')
def read_user_by_id(user_id):
    """
    Get a specific user by id.
    """
    user = user_services.get_by_id(id=user_id)
    # user = user_redis_decorator.get(db, id=user_id)
    if not user:
        raise error.HTTPError(
            code=404, msg="User not found", url=None,
            hdrs=None, fp=None)

    print(user)


if __name__ == '__main__':
    read_user_by_id()
