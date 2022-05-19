from app.api.dependencies.post_services import get_post_services

post_services = get_post_services()


def update_view(msg):
    post_services.update_views(msg['id'])
