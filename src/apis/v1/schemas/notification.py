from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateNotificationRequest(BaseModel):
    notification_id: int
    booking_id: int
    message:str
    is_read:bool
    level:str


class FindNotificationRequest(BaseModel):
    notification_id: Optional[int] =None
    booking_id: Optional[int] =None
    message: Optional[str] =None
    is_read: Optional[bool] =None
    level: Optional[str] =None
