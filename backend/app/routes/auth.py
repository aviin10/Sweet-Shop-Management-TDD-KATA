from fastapi import APIRouter, status, HTTPException
from app.schemas.user import UserCreate
from app.services.user_service import create_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    result = await create_user(
        email=user.email,
        password=user.password,
        role=user.role
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    return result
