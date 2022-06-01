from fastapi.testclient import TestClient

from app.models import Post
from app.config import settings


class TestPost:

    def test_create_post(
        self,
        client: TestClient,
        superuser_token_headers: dict
    ) -> None:
        data = {"title": "Foo", "body": "Fighters", "tagList": ["boxing"]}
        response = client.post(
            f"{settings.API_V1_STR}/posts/",
            headers=superuser_token_headers, json=data,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["title"] == data["title"]
        assert content["body"] == data["body"]
        assert "id" in content
        assert "views" in content
        assert "author" in content
        assert "favorited" in content
        assert "favorites_count" in content

    def test_read_post(
        self,
        client: TestClient,
        superuser_token_headers: dict,
        random_post: Post
    ) -> None:
        post = random_post

        response = client.get(
            f"{settings.API_V1_STR}/posts/{post.id}",
            headers=superuser_token_headers,
        )

        assert response.status_code == 200
        content = response.json()
        assert content["title"] == post.title
        assert content["body"] == post.body
        assert content["id"] == post.id
        assert content["author"]["id"] == post.author_id
