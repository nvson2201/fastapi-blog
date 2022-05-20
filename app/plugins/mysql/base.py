# Import all the models, so that Base has them before being
# imported by Alembic
from app.plugins.mysql.base_class import Base  # noqa
from app.models.posts import Post  # noqa
from app.models.users import User  # noqa
from app.models.comments import Comment  # noqa
