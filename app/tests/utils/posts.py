import random
from app.config import settings

from app.models import Post
from app.tests.utils.users import random_user
from app.tests.utils.utils import random_lower_string


def random_post() -> Post:
    user = random_user()
    post = Post()
    post.id = random.randint(1, 1000000)
    post.views = 0
    post.title = random_lower_string()
    post.body = random_lower_string()
    post.created_at = settings.current_time()
    post.updated_at = user.created_at
    post.author_id = user.id

    return post
