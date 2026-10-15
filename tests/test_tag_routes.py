import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def empty_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("repositories.tags._TAGS", {})


def test_post_tags_returns_201_and_created_tag() -> None:
    response = client.post("/tags", json={"name": "urgent"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "urgent"}


def test_post_tags_assigns_next_id() -> None:
    client.post("/tags", json={"name": "urgent"})
    response = client.post("/tags", json={"name": "home"})
    assert response.status_code == 201
    assert response.json() == {"id": 2, "name": "home"}


def test_post_tags_rejects_duplicate_ignoring_case_and_whitespace() -> None:
    client.post("/tags", json={"name": "Urgent"})
    response = client.post("/tags", json={"name": " urgent "})
    assert response.status_code == 400
    assert response.json() == {"detail": "Tag 'urgent' already exists."}


def test_post_tags_rejects_blank_name() -> None:
    response = client.post("/tags", json={"name": "   "})
    assert response.status_code == 400
    assert response.json() == {"detail": "Tag name cannot be empty."}


def test_post_tags_rejects_missing_name() -> None:
    response = client.post("/tags", json={})
    assert response.status_code == 422
