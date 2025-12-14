from app.db.mongodb import get_database

async def init_indexes():
    db = await get_database()
    await db["users"].create_index("email", unique=True)
