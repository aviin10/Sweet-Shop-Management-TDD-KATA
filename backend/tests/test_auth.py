import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_user_registration_success(monkeypatch):
    async def mock_create_user(email, password, role):
        return {"email": email, "role": role}

    # ✅ PATCH WHERE IT IS USED
    monkeypatch.setattr(
        "app.routes.auth.create_user",
        mock_create_user
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "unique@example.com",
                "password": "secret123",
                "role": "user"
            }
        )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_user_registration_duplicate_email(monkeypatch):
    async def mock_create_user(email, password, role):
        return None  # simulate duplicate

    # ✅ SAME PATCH HERE
    monkeypatch.setattr(
        "app.routes.auth.create_user",
        mock_create_user
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "secret123",
                "role": "user"
            }
        )

    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_success(monkeypatch):
    async def mock_get_user(email):
        return {
            "email": email,
            "password": "$2b$12$dummyhash",
            "role": "user"
        }

    async def mock_verify_password(password, hashed):
        return True

    monkeypatch.setattr("app.routes.auth.get_user_by_email", mock_get_user)
    monkeypatch.setattr("app.routes.auth.verify_password", mock_verify_password)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "secret123"
            }
        )

    assert response.status_code == 200
    assert "access_token" in response.json()
