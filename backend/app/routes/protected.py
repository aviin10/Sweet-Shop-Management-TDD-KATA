from fastapi import APIRouter, Depends
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/protected", tags=["Protected"])

@router.get("/me")
async def read_me(current_user=Depends(get_current_user)):
    return current_user
