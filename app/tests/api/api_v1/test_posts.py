from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.tests.utils.posts import create_random_post


def test_create_post(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "body": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/posts/",
        headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["body"] == data["body"]
    assert "id" in content
    assert "author_id" in content


def test_read_post(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    post = create_random_post(db)
    response = client.get(
        f"{settings.API_V1_STR}/posts/{post.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == post.title
    assert content["body"] == post.body
    assert content["id"] == post.id
    assert content["author_id"] == post.author_id
