from fastapi import HTTPException, status
from app.db.mongodb import get_database
from bson import ObjectId


async def purchase_sweet_service(id: str):
    db = await get_database()
    sweets = db["sweets"]

    sweet = await sweets.find_one({"_id": ObjectId(id)})

    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )

    if sweet["quantity"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sweet out of stock"
        )

    await sweets.update_one(
        {"_id": ObjectId(id)},
        {"$inc": {"quantity": -1}}
    )

    sweet["quantity"] -= 1
    sweet["id"] = str(sweet["_id"])
    sweet.pop("_id")

    return sweet


async def restock_sweet_service(id: str, quantity: int):
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero"
        )

    db = await get_database()
    sweets = db["sweets"]

    sweet = await sweets.find_one({"_id": ObjectId(id)})

    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )

    await sweets.update_one(
        {"_id": ObjectId(id)},
        {"$inc": {"quantity": quantity}}
    )

    sweet["quantity"] += quantity
    sweet["id"] = str(sweet["_id"])
    sweet.pop("_id")

    return sweet
