from app.api.dependencies.database import get_db
from app.services.posts import PostServices
from app.db.repositories_cache.posts import PostRedisRepository
from app.db import repositories
from app.config import settings
from app.schemas.post import PostUpdateView
from app.plugins.redis import redis_services

crud_engine = PostRedisRepository(
    repositories.posts, settings.REDIS_PREFIX_POST
)
db = next(get_db())
post_services = PostServices(db, crud_engine=crud_engine)


def update_view(post):
    id = post['id']
    views = post['views']
    post_view = PostUpdateView(id=id, views=views)

    cache_data = redis_services.get_cache(
        id, settings.REDIS_PREFIX_POST_VIEWS
    )

    if cache_data:
        post_view.views = cache_data['views'] + 1
    else:
        post_view.views += 1

    redis_services.set_cache(
        id, settings.REDIS_PREFIX_POST_VIEWS,
        post_view.__dict__
    )

    post_services.update(id=post_view.id, body=post_view)
