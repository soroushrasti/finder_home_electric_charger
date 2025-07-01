from typing import Optional
from pydantic import BaseModel

class CreatePricingRequest(BaseModel):
    pricing_id: int
    booking_id: int
    currency: str
    total_value: float
    price_per_khw: float

class FindPricingRequest(BaseModel):
    charger_location_owner_user_id :Optional[int] =None
    car_owner_user_id : Optional[int] =None
    pricing_id: Optional[int] =None
    booking_id: Optional[int] =None
    currency: Optional[str] =None
    total_value: Optional[complex] =None
    price_per_khw: Optional[complex] =None
