from fastapi import APIRouter, status
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    hashed = hash_password(user.password)

    return {
        "email": user.email,
        "role": user.role
    }
