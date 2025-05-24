from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserType(str, Enum):
    HOMEOWNER = "HOMEOWNER"
    ELECTRIC_CAR_OWNER = "ELECTRIC_CAR_OWNER"

class CreateUserRequest(BaseModel):
    username: str
    first_name: str = Field(..., alias="firstName")
    password: str = Field(default="")
    last_name: str = Field(..., alias="lastName")
    email: EmailStr
    address_of_home: str = Field(..., alias="address")
    city_of_home: str = Field(..., alias="city")
    postcode_of_home: str = Field(..., alias="postCode")
    user_type: UserType = Field(..., alias="userType")
    mobile_number: str = Field(..., alias="mobile")

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True