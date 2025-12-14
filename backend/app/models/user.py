from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserInDB(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    password: str
    role: str
