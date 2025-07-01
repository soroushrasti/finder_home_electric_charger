from typing import Optional
from pydantic import BaseModel


class FindActivityRequest(BaseModel):
    charger_location_owner_user_id :Optional[int] =None
    car_owner_user_id : Optional[int] =None
