# Import all the models, so that Base has them before being
# imported by Alembic
from app.plugins.mysql.base_class import Base  # noqa
from app.models.post import Post  # noqa
from app.models.user import User  # noqa
from app.models.comment import Comment  # noqa