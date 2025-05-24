from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserType(str, Enum):
    HOMEOWNER = "Homeowner"
    ELECTRIC_CAR_OWNER = "Electric car owner"

class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    password: str
    last_name: str
    email: EmailStr
    address_of_home: str
    city_of_home: str
    post_code_of_home: str
    user_type: UserType
    mobile_number: str