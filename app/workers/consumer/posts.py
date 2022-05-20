from app.services.posts import post_redis_services


def update_view(msg):
    post_redis_services.update_views(msg['id'])
