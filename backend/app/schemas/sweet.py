from pydantic import BaseModel
from typing import Optional

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetOut(SweetCreate):
    id: Optional[str]
