from app.db.mongodb import get_database
from bson import ObjectId
from pymongo import ReturnDocument
async def create_sweet(data: dict):
    db = await get_database()
    result = await db["sweets"].insert_one(data)
    return {**data, "id": str(result.inserted_id)}

async def list_sweets():
    db = await get_database()
    sweets = []
    async for s in db["sweets"].find():
        s["id"] = str(s["_id"])
        sweets.append(s)
    return sweets
async def search_sweets(filters: dict):
    db = await get_database()
    query = {}

    if "name" in filters:
        query["name"] = {"$regex": filters["name"], "$options": "i"}

    if "category" in filters:
        query["category"] = filters["category"]

    if "min_price" in filters or "max_price" in filters:
        query["price"] = {}
        if filters.get("min_price") is not None:
            query["price"]["$gte"] = filters["min_price"]
        if filters.get("max_price") is not None:
            query["price"]["$lte"] = filters["max_price"]

    sweets = []
    async for s in db["sweets"].find(query):
        s["id"] = str(s["_id"])
        sweets.append(s)

    return sweets


async def update_sweet(id: str, data: dict):
    db = await get_database()
    await db["sweets"].update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return {**data, "id": id}

async def delete_sweet(id: str):
    db = await get_database()
    await db["sweets"].delete_one({"_id": ObjectId(id)})
    return True

async def purchase_sweet(id: str):
    db = await get_database()

    sweet = await db["sweets"].find_one_and_update(
        {"_id": ObjectId(id), "quantity": {"$gt": 0}},
        {"$inc": {"quantity": -1}},
        return_document=ReturnDocument.AFTER
    )

    if not sweet:
        return None

    sweet["id"] = str(sweet["_id"])
    return sweet


async def restock_sweet(id: str, quantity: int):
    db = await get_database()

    sweet = await db["sweets"].find_one_and_update(
        {"_id": ObjectId(id)},
        {"$inc": {"quantity": quantity}},
        return_document=ReturnDocument.AFTER
    )

    if not sweet:
        return None

    sweet["id"] = str(sweet["_id"])
    return sweet