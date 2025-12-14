from fastapi import APIRouter, status, HTTPException
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.core.security import create_access_token
from app.services.user_service import get_user_by_email
from app.services.auth_service import verify_password

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
@router.post("/login")
async def login_user(data: dict):
    user = await get_user_by_email(data["email"])

    if not user or not verify_password(data["password"], user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["email"],
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}