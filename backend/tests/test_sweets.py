import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_add_sweet_admin_only(monkeypatch):
    async def mock_create_sweet(data):
        return {**data, "id": "123"}

    monkeypatch.setattr(
        "app.routes.sweets.create_sweet",
        mock_create_sweet
    )

    admin_token = create_access_token({
        "sub": "admin@example.com",
        "role": "admin"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/sweets",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "name": "Rasgulla",
                "category": "Indian",
                "price": 20,
                "quantity": 50
            }
        )

    assert response.status_code == 201
    assert response.json()["name"] == "Rasgulla"


@pytest.mark.asyncio
async def test_list_sweets(monkeypatch):
    async def mock_list_sweets():
        return [
            {
                "id": "1",
                "name": "Ladoo",
                "category": "Indian",
                "price": 10,
                "quantity": 100
            }
        ]

    monkeypatch.setattr(
        "app.routes.sweets.list_sweets",
        mock_list_sweets
    )

    user_token = create_access_token({
        "sub": "user@example.com",
        "role": "user"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {user_token}"}
        )

    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_search_sweets(monkeypatch):
    async def mock_search_sweets(filters):
        return [
            {
                "id": "1",
                "name": "Kaju Katli",
                "category": "Indian",
                "price": 50,
                "quantity": 20
            }
        ]

    monkeypatch.setattr(
        "app.routes.sweets.search_sweets",
        mock_search_sweets
    )

    token = create_access_token({
        "sub": "user@example.com",
        "role": "user"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/sweets/search?name=Kaju",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Kaju Katli"


@pytest.mark.asyncio
async def test_update_sweet_admin(monkeypatch):
    async def mock_update_sweet(id, data):
        return {**data, "id": id}

    monkeypatch.setattr(
        "app.routes.sweets.update_sweet",
        mock_update_sweet
    )

    admin_token = create_access_token({
        "sub": "admin@example.com",
        "role": "admin"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.put(
            "/api/sweets/123",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "name": "Updated Sweet",
                "category": "Indian",
                "price": 40,
                "quantity": 30
            }
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_sweet_admin(monkeypatch):
    async def mock_delete_sweet(id):
        return True

    monkeypatch.setattr(
        "app.routes.sweets.delete_sweet",
        mock_delete_sweet
    )

    admin_token = create_access_token({
        "sub": "admin@example.com",
        "role": "admin"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(
            "/api/sweets/123",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

    assert response.status_code == 204
