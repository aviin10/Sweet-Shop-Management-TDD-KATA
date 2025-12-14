import pytest
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

@pytest.mark.asyncio
async def test_database_instance():
    db = await get_database()
    assert isinstance(db, AsyncIOMotorDatabase)
