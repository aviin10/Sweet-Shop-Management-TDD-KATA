from fastapi import APIRouter, Depends
from app.core.deps import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/dashboard")
async def admin_dashboard(admin=Depends(require_admin)):
    return {
        "message": "Welcome admin",
        "email": admin["email"]
    }
