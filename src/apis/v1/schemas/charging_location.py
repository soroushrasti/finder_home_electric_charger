from typing import Optional
from pydantic import BaseModel, Field

class CreateChargingLocRequest(BaseModel):
    user_id: int
    post_code: Optional[str] = None
    city: Optional[str] = None
    alley: Optional[str] = None
    street: Optional[str] = None
    home_phone_number: Optional[str] = None
    fast_charging: Optional[bool] = False  # Fast charging option as a boolean
    description: Optional[str] = None
    price_per_hour: Optional[float] = None
    power_output: Optional[float] = None  # in kW
    name: Optional[str] = None
    currency: Optional[str] = "Rials"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    country: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


from pydantic import BaseModel, Field

class ChargingLocResponse(BaseModel):
    street: str
    user_id: int = Field(..., alias="userId")
    post_code: str = Field(..., alias="postCode")
    city: str
    alley: str
    charging_location_id: int = Field(..., alias="chargingLocationId")
    home_phone_number: str = Field(..., alias="homePhoneNumber")
    fast_charging: bool = Field(..., alias="fastCharging")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

class FindChargingLocRequest(BaseModel):
        post_code :Optional[str] =None
        alley:Optional[str] =None
        street :Optional[str] =None
        home_phone_number :Optional[str] =None
        city :Optional[str] =None
        fast_charging :Optional[bool] =False
        user_id :Optional[int] =None
        description: Optional[str] = None
        price_per_hour: Optional[float] = None
        power_output: Optional[float] = None  # in kW
        name: Optional[str] = None
        currency: Optional[str] = "Rials"
        country: Optional[str] = None
        latitude: Optional[float] = None
        longitude: Optional[float] = None
        review_number : Optional[int] = None
        review_average: Optional[float] = None

class UpdateChargingLocRequest(BaseModel):
    user_id: int
    post_code: Optional[str] = None
    city: Optional[str] = None
    alley: Optional[str] = None
    street: Optional[str] = None
    home_phone_number: Optional[str] = None
    fast_charging: Optional[bool] = False  # Fast charging option as a boolean
    description: Optional[str] = None
    price_per_hour: Optional[float] = None
    power_output: Optional[float] = None  # in kW
    name: Optional[str] = None
    currency: Optional[str] = "Rials"
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FindNearbyChargingLocRequest(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = 1000000
