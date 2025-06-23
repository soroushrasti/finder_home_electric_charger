from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateBookingRequest(BaseModel):
    user_id: int
    charging_location_id: int
    review_rate:datetime
    start_time:datetime
    end_time:datetime
    review_message: str


class FindBookingRequest(BaseModel):
    booking_id: Optional[int] =None
    user_id: Optional[int] =None
    charging_location_id: Optional[int] =None
    review_rate: Optional[datetime] =None
    start_time: Optional[datetime] =None
    end_time: Optional[datetime] =None
    endreview_message: Optional[str] =None
