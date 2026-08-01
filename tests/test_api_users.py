"""
tests/test_api_users.py

Demonstrates the ApiClient wrapper: retry-aware, logged, config-driven
base URL - no raw requests.get() calls scattered across test files.

Uses JSONPlaceholder (jsonplaceholder.typicode.com) - a long-standing,
stable, no-auth-required fake REST API built for exactly this kind of
testing practice.
"""


def test_get_single_post_returns_expected_schema(api_client):
    resp = api_client.get("/posts/1")
    assert resp.status_code == 200

    body = resp.json()
    assert set(["id", "userId", "title", "body"]).issubset(body.keys())
    assert body["id"] == 1


def test_get_nonexistent_post_returns_404(api_client):
    resp = api_client.get("/posts/9999")
    assert resp.status_code == 404


def test_create_post_returns_201_with_echoed_fields(api_client):
    resp = api_client.post(
        "/posts",
        json_body={"title": "SDET framework test", "body": "created via ApiClient", "userId": 1},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "SDET framework test"
    assert "id" in body


def test_update_post_returns_updated_fields(api_client):
    resp = api_client.put(
        "/posts/1",
        json_body={"id": 1, "title": "Updated title", "body": "Updated body", "userId": 1},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated title"


def test_delete_post_returns_200(api_client):
    resp = api_client.delete("/posts/1")
    assert resp.status_code == 200
