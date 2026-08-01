"""
tests/test_api_users.py

Demonstrates the ApiClient wrapper: retry-aware, logged, config-driven
base URL - no raw requests.get() calls scattered across test files.
"""


def test_get_single_user_returns_expected_schema(api_client):
    resp = api_client.get("/users/2")
    assert resp.status_code == 200

    body = resp.json()["data"]
    assert set(["id", "email", "first_name", "last_name"]).issubset(body.keys())
    assert body["id"] == 2


def test_get_nonexistent_user_returns_404(api_client):
    resp = api_client.get("/users/9999")
    assert resp.status_code == 404


def test_create_user_returns_201_with_echoed_fields(api_client):
    resp = api_client.post("/users", json_body={"name": "Sankalp", "job": "SDET"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Sankalp"
    assert "id" in body
    assert "createdAt" in body
