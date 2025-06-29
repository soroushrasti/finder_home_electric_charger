from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class UserType(str, Enum):
    HOMEOWNER = "Home owner"
    ELECTRIC_CAR_OWNER = "Electric car owner"
class UserLogin(BaseModel):
    email: str = Field(..., alias="email")
    password: str = Field(..., alias="password")

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True

class CreateUserRequest(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    password: str = None
    last_name: Optional[str] = None
    email: EmailStr
    address_of_home: Optional[str] = None
    city_of_home: Optional[str] = None
    postcode_of_home: Optional[str] = None
    user_type: UserType
    mobile_number: Optional[str]  = None

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True