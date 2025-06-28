from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateBookingRequest(BaseModel):
    car_id: int
    charging_location_id: int
    review_rate:Optional[datetime]
    review_message: Optional[str]


class FindBookingRequest(BaseModel):
    charger_location_owner_user_id :Optional[int] =None
    car_owner_user_id : Optional[int] =None
    car_id: Optional[int] =None
    charging_location_id: Optional[int] =None
    review_rate: Optional[datetime] =None
    start_time: Optional[datetime] =None
    end_time: Optional[datetime] =None
    review_message: Optional[str] =None

class UpdateBookingRequest(BaseModel):
    user_id: Optional[int] =None
    charging_location_id: Optional[int] =None
    start_time: Optional[datetime] =None
    end_time: Optional[datetime] =None
    review_message: Optional[str] =None
    review_rate: Optional[str] =None

class AddBookingRequest(BaseModel):
    start_time: Optional[datetime] =None
    end_time: Optional[datetime] =None
