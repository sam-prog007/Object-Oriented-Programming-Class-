import pytest
from fastapi.testclient import TestClient

from main import API_KEY, app, get_repository
from repository import InMemoryBookRepository

AUTH = {"X-API-Key": API_KEY}
BOOK = {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008}


@pytest.fixture
def client():
    """A fresh repository for every test, injected through dependency_overrides."""
    repo = InMemoryBookRepository()
    app.dependency_overrides[get_repository] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_home(client):
    assert client.get("/").status_code == 200


def test_list_starts_empty(client):
    assert client.get("/books").json() == []


def test_create_and_get(client):
    created = client.post("/books", json=BOOK, headers=AUTH)
    assert created.status_code == 201
    book_id = created.json()["id"]
    assert client.get(f"/books/{book_id}").json() == {**BOOK, "id": book_id}


def test_create_requires_api_key(client):
    assert client.post("/books", json=BOOK).status_code == 401
    assert client.post("/books", json=BOOK, headers={"X-API-Key": "wrong"}).status_code == 401


def test_validation_error(client):
    bad = {**BOOK, "year": -5}
    assert client.post("/books", json=bad, headers=AUTH).status_code == 422


def test_update(client):
    book_id = client.post("/books", json=BOOK, headers=AUTH).json()["id"]
    updated = client.put(f"/books/{book_id}", json={**BOOK, "year": 2009}, headers=AUTH)
    assert updated.json()["year"] == 2009


def test_delete(client):
    book_id = client.post("/books", json=BOOK, headers=AUTH).json()["id"]
    assert client.delete(f"/books/{book_id}", headers=AUTH).status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_unknown_book_is_404(client, method):
    kwargs = {"headers": AUTH}
    if method == "put":
        kwargs["json"] = BOOK
    assert getattr(client, method)("/books/999", **kwargs).status_code == 404


def test_route_uses_injected_repository(mocker):
    """Mock the repository entirely: the route must just call repo.list()."""
    fake_repo = mocker.Mock()
    fake_repo.list.return_value = []
    app.dependency_overrides[get_repository] = lambda: fake_repo
    try:
        TestClient(app).get("/books")
    finally:
        app.dependency_overrides.clear()
    fake_repo.list.assert_called_once_with()


def test_decorators_registered_the_routes():
    routes = {(r.path, m) for r in app.routes for m in getattr(r, "methods", [])}
    assert ("/books", "GET") in routes and ("/books", "POST") in routes
    assert ("/books/{book_id}", "DELETE") in routes
