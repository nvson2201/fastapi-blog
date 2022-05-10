from urllib import error

import click

from app.api.dependencies.database import get_db
from app.services.user import UserServices
from app.db.repositories_cache.user import CRUDRedisUserDecorator
from app.config import settings
from app.db import repositories

db = next(get_db())

crud_engine = CRUDRedisUserDecorator(
    repositories.user, settings.REDIS_SUFFIX_USER
)

user_services = UserServices(db, crud_engine=crud_engine)


@click.command()
@click.option('--user_id', prompt='user_id')
def read_user_by_id(user_id):
    """
    Get a specific user by id.
    """
    user = user_services.get_by_id(id=user_id)
    if not user:
        raise error.HTTPError(
            code=404, msg="User not found", url=None,
            hdrs=None, fp=None)

    print(user)


if __name__ == '__main__':
    read_user_by_id()
