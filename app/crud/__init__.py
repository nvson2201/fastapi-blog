from .crud_post import post  # noqa
from .crud_user import user  # noqa
from .crud_comment import comment  # noqa
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.post import Post
# from app.schemas.post import PostCreate, PostUpdate

# post = CRUDBase[Post, PostCreate, PostUpdate](Post)
