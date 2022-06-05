from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from app.config import settings

from app.models import Post
from app.schemas.posts import PostInDB
from app.db.repositories.posts import PostRepository
from app.tests.utils.utils import random_lower_string
from app.tests.utils.users import random_user
from app.tests.utils.posts import random_post


class TestPostRepository:

    def test_get_post(self) -> None:
        id = 1
        db = UnifiedAlchemyMagicMock()

        PostRepository(db).get(id=id)

        db.query.assert_called_once_with(Post)
        db.filter.assert_called_once_with(Post.id == id)

    def test_create_post(self) -> None:
        db = UnifiedAlchemyMagicMock()
        title = random_lower_string()
        body = random_lower_string()
        created_at = settings.current_time()
        updated_at = created_at
        user = random_user()
        post_body = PostInDB(
            title=title,
            body=body,
            author_id=user.id,
            created_at=created_at,
            updated_at=updated_at,
            views=0
        )

        PostRepository(db).create(body=post_body)

        db.add.assert_called()
        db.refresh.assert_called()
        db.commit.assert_called()

    def test_update_post(self) -> None:
        db = UnifiedAlchemyMagicMock()
        post = random_post()
        post_body = PostInDB(
            title=random_lower_string(),
            body=random_lower_string()
        )

        PostRepository(db).update(post, body=post_body)
        db.merge.assert_called()
        db.commit.assert_called()

    def test_delete_post(self) -> None:
        db = UnifiedAlchemyMagicMock()
        post = random_post()
        db.query.return_value.get.side_effect = [post]

        PostRepository(db).remove(id=post.id)
        db.query.assert_called_once_with(Post)
        db.delete.assert_called_once_with(post)
        db.commit.assert_called_once_with()
