from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateChargingLocRequest(BaseModel):
    user_id: int
    post_code: int
    alley: str
    street: str
    city: str
    home_phone_number: int
    fast_charging: bool
