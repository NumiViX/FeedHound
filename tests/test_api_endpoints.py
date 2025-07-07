import os
import datetime
import pytest
from fastapi.testclient import TestClient

# ensure database URL for app import
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from app.main import app
from app.db.session import get_async_session


@pytest.fixture()
async def client(async_session):
    async def override_session():
        yield async_session
    app.dependency_overrides[get_async_session] = override_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sources_endpoints(client):
    create_data = {
        "title": "Example",
        "url": "http://example.com",
        "rss_url": "http://example.com/rss",
    }
    resp = client.post("/api/v1/sources/", json=create_data)
    assert resp.status_code == 200
    src = resp.json()
    assert src["id"]
    src_id = src["id"]

    resp = client.get(f"/api/v1/sources/{src_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == src_id

    resp = client.get("/api/v1/sources/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.get("/api/v1/sources/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_news_endpoints(client):
    src_resp = client.post(
        "/api/v1/sources/",
        json={"title": "Src", "url": "http://s.com", "rss_url": "http://s.com/rss"},
    )
    src_id = src_resp.json()["id"]

    news_data = {
        "title": "News1",
        "url": "http://s.com/n1",
        "published_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_id": src_id,
    }
    resp = client.post("/api/v1/news/", json=news_data)
    assert resp.status_code == 201
    news = resp.json()
    news_id = news["id"]

    resp = client.get(f"/api/v1/news/{news_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == news_id

    resp = client.get("/api/v1/news/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.get("/api/v1/news/999")
    assert resp.status_code == 404

    update_data = {
        "title": "Updated",
        "url": "http://s.com/n2",
        "published_at": news_data["published_at"],
        "source_id": src_id,
    }
    put_resp = client.put(f"/api/v1/news/{news_id}", json=update_data)
    assert put_resp.status_code == 200
    assert put_resp.json()["title"] == "Updated"


@pytest.mark.asyncio
async def test_auth_and_user_me(client):
    user_data = {
        "email": "user@example.com",
        "username": "user",
        "password": "secret",
    }
    resp = client.post("/api/v1/auth/register", json=user_data)
    assert resp.status_code == 200
    user = resp.json()
    assert user["email"] == user_data["email"]

    dup_resp = client.post("/api/v1/auth/register", json=user_data)
    assert dup_resp.status_code == 400

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "user", "password": "secret"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    wrong_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "user", "password": "wrong"},
    )
    assert wrong_resp.status_code == 400

    me_resp = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "user"
