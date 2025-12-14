import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_admin_access_allowed():
    token = create_access_token({
        "sub": "admin@example.com",
        "role": "admin"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/admin/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_admin_access_denied_for_user():
    token = create_access_token({
        "sub": "user@example.com",
        "role": "user"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/admin/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 403
