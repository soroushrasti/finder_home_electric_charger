from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateCarRequest(BaseModel):
    user_id: int
    model: str
    color: str
    year: int
    license_plate: str


class FindCarRequest(BaseModel):
    user_id: Optional[int] =None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    license_plate: Optional[str] = None
