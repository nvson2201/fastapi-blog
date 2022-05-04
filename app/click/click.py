import click

from app.plugins.redis import redis_services
from app.config import settings
from app.api import deps
from app import crud
from urllib import error
from app.models.user import User

db = next(deps.get_db())


@click.command()
@click.option('--user_id', prompt='user_id')
def read_user_by_id(user_id):
    """
    Get a specific user by id.
    """
    # cache hit
    cache_data = redis_services.get_cache(
        id=str(user_id),
        suffix=settings.REDIS_SUFFIX_USER
    )
    if cache_data:
        user = User(**cache_data)
    # cache miss
    else:
        user = crud.user.get(db, id=user_id)
        if not user:
            raise error.HTTPError(
                code=404, msg="User not found", url=None,
                hdrs=None, fp=None)

        # write to cache
        redis_services.set_cache(
            id=str(user_id),
            suffix="user_id",
            data=user.__dict__
        )

    print(user)


if __name__ == '__main__':
    read_user_by_id()
