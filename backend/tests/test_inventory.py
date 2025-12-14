import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_purchase_sweet_success(monkeypatch):
    async def mock_purchase_sweet(id):
        return {"id": id, "quantity": 4}

    monkeypatch.setattr(
    "app.routes.sweets.purchase_sweet_service",
    mock_purchase_sweet
)


    token = create_access_token({
        "sub": "user@example.com",
        "role": "user"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/sweets/123/purchase",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_restock_sweet_admin(monkeypatch):
    async def mock_restock_sweet(id, qty):
        return {"id": id, "quantity": 10}

    monkeypatch.setattr(
        "app.routes.sweets.restock_sweet_service",
        mock_restock_sweet
    )

    admin_token = create_access_token({
        "sub": "admin@example.com",
        "role": "admin"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/sweets/123/restock?quantity=5",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

    assert response.status_code == 200
