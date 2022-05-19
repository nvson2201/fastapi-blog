from collections import defaultdict

from app.api.dependencies.database import get_db
from app.services.posts import PostServices
from app.db.repositories_cache.posts import PostRedisRepository
from app.db import repositories
from app.config import settings
from app.schemas.post import PostUpdateView

crud_engine = PostRedisRepository(
    repositories.posts, settings.REDIS_SUFFIX_POST
)
db = next(get_db())
post_services = PostServices(db, crud_engine=crud_engine)


def update_view(posts):
    views_counted_list = defaultdict(int)
    for post in posts:
        views_counted_list[post['id']] = post['views']

    for post in posts:
        views_counted_list[post['id']] += 1

    for id, views in views_counted_list.items():
        obj_in = PostUpdateView(id=int(id), views=views)
        post_services.update(id=int(id), obj_in=obj_in)
