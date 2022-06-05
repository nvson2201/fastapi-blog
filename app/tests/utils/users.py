import random

from app.models.users import User

from app.config import settings
from app.tests.utils.utils import (
    random_email, random_password, random_lower_string)
from app.utils.security import get_password_hash


def random_user() -> User:
    user = User()
    user.id = random.randint(1, 1000000)
    user.email = random_email()
    user.username = random_lower_string()
    user.hashed_password = get_password_hash(random_password())
    user.created_at = settings.current_time()
    user.updated_at = user.created_at
    user.is_active = True
    user.is_superuser = False
    user.is_banned = False

    return user
