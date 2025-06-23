from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateBookingRequest(BaseModel):
    booking_id:int
    user_id: int
    charging_location_id: int
    review_rate:datetime
    startDate:datetime
    endDate:datetime
    review_message: str


class FindBookingRequest(BaseModel):
    booking_id: Optional[int] =None
    user_id: Optional[int] =None
    charging_location_id: Optional[int] =None
    review_rate: Optional[datetime] =None
    startDate: Optional[datetime] =None
    endDate: Optional[datetime] =None
    endreview_message: Optional[str] =None
