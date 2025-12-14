from fastapi import APIRouter, Depends, status, Query, HTTPException
from app.services.inventory_service import (
    purchase_sweet_service,
    restock_sweet_service
)
from app.schemas.sweet import SweetCreate
from app.core.deps import get_current_user, require_admin
from app.services.sweet_service import create_sweet, list_sweets

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_sweet(
    sweet: SweetCreate,
    admin=Depends(require_admin)
):
    return await create_sweet(sweet.dict())

@router.get("")
async def get_sweets(
    user=Depends(get_current_user)
):
    return await list_sweets()

@router.get("/search")
async def search_sweets(
    name: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    user=Depends(get_current_user)
):
    filters = {
        k: v for k, v in {
            "name": name,
            "category": category,
            "min_price": min_price,
            "max_price": max_price
        }.items() if v is not None
    }

    return await search_sweets(filters)


@router.put("/{id}")
async def update_sweet(
    id: str,
    sweet: SweetCreate,
    admin=Depends(require_admin)
):
    return await update_sweet(id, sweet.dict())


@router.delete("/{id}", status_code=204)
async def delete_sweet(
    id: str,
    admin=Depends(require_admin)
):
    await delete_sweet(id)

@router.post("/{id}/purchase")
async def purchase_sweet(
    id: str,
    current_user=Depends(get_current_user)
):
    return await purchase_sweet_service(id)


@router.post("/{id}/restock")
async def restock_sweet(
    id: str,
    quantity: int,
    current_user=Depends(require_admin)
):
    return await restock_sweet_service(id, quantity)