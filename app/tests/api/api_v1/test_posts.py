from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies.services import get_post_services
from app.config import settings


post_example = {
    "id": 1,
    "title": "Foo",
    "body": "Fighters",
    "author": {
        "id": 1,
        "username": "admin",
        "email": "n.vanson.2201@gapo.com.vn"
    },
    "tagList": ["boxing"],
    "favorited": False,
    "favorites_count": 0,
}


@pytest.fixture(scope="class")
def post_services():
    mock_post_services = MagicMock()
    app.dependency_overrides[get_post_services] = \
        lambda: mock_post_services
    yield mock_post_services
    app.dependency_overrides = {}


class TestPost:

    @pytest.mark.usefixtures("override_superuser")
    def test_create_post(
        self,
        post_services,
        client: TestClient
    ) -> None:
        data = {"title": "Foo", "body": "Fighters", "tagList": ["boxing"]}

        post_services.create_with_owner.return_value = post_example
        response = client.post(
            f"{settings.API_V1_STR}/posts/",
            headers={}, json=data,
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

    @pytest.mark.usefixtures("override_superuser")
    def test_read_post(
        self, post_services, client: TestClient
    ) -> None:

        post_services.get.return_value = post_example
        id = post_example["id"]
        response = client.get(
            f"{settings.API_V1_STR}/posts/{id}",
            headers={},
        )

        assert response.status_code == 200
        content = response.json()

        assert content["title"] == post_example["title"]
        assert content["body"] == post_example["body"]
        assert content["id"] == post_example["id"]
        assert content["author"]["id"] == post_example["author"]["id"]
