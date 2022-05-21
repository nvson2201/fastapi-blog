from app.services.posts import post_services


def update_view(msg):
    post_services.update_views(msg['id'])
