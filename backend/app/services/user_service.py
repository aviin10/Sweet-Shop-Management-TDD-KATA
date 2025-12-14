from pymongo.errors import DuplicateKeyError
from app.db.mongodb import get_database
from app.services.auth_service import hash_password

async def create_user(email: str, password: str, role: str):
    db = await get_database()
    users = db["users"]

    user_doc = {
        "email": email,
        "password": hash_password(password),
        "role": role,
    }

    try:
        await users.insert_one(user_doc)
    except DuplicateKeyError:
        return None

    return {
        "email": email,
        "role": role
    }
async def get_user_by_email(email: str):
    db = await get_database()
    return await db["users"].find_one({"email": email})
