from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class UserType(PyEnum):
    HOMEOWNER = "Homeowner"
    ELECTRIC_CAR_OWNER = "Electric car owner"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address_of_home = Column(Text, nullable=False)
    city_of_home = Column(String(100), nullable=False)
    postcode_of_home = Column(String(20), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    mobile_number = Column(String(15), nullable=False)