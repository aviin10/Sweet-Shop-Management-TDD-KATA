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
