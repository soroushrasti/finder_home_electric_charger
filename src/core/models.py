from numbers import Complex

from sqlalchemy import Column, Integer,Float, String, Enum, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    address_of_home = Column(Text, nullable=True)
    city_of_home = Column(String(100), nullable=True)
    postcode_of_home = Column(String(20), nullable=True)
    user_type = Column(String(20), nullable=False)
    mobile_number = Column(String(15), nullable=True)


class Car(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Foreign key to User
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(30), nullable=False)
    license_plate = Column(String(15), unique=True, nullable=False)  # Unique license plate


class ChargingLocation(Base):
    __tablename__ = 'charging_locations'

    charging_location_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Foreign key to User
    post_code = Column(String(20), nullable=True)
    alley = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    home_phone_number = Column(String(15), nullable=True)
    city = Column(String(100), nullable=True)  # City of the charging location
    fast_charging = Column(Boolean, nullable=True)  # Fast charging option as a string (e.g., "Yes" or "No")
    name = Column(String(100), nullable=True)  # Name of the charging location
    price_per_hour = Column(Float, nullable=True)  # Price per hour for charging
    power_output = Column(Float, nullable=True)
    description = Column(Text, nullable=True)  # Description of the charging location


class Booking(Base):
    __tablename__ = 'booking'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('cars.car_id'), nullable=True)  # Foreign key to cars
    charging_location_id = Column(Integer, ForeignKey('charging_locations.charging_location_id'), nullable=False)  # Foreign key to ChargingLocation
    start_time = Column(DateTime, nullable=False)  # Start time of the booking
    end_time = Column(DateTime, nullable=True)  # End time of the booking
    review_rate = Column(Integer, nullable=True)  # Review rating (1-5)
    review_message = Column(Text, nullable=True)  # Review message

class Notification(Base):
    __tablename__ = 'notification'

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('booking.booking_id'), nullable=False)  # Foreign key to booking
    message = Column(Text, nullable=True)  # message
    level = Column(Text, nullable=True)  # level
    is_read = Column(Boolean, nullable=True)  # is_read


class Review(Base):
    __tablename__ = 'review'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    review_rate = Column(Integer, nullable=True)
    review_message = Column(Text, nullable=True)
    car_id = Column(Integer, ForeignKey('cars.car_id'), nullable=False)
    charging_location_id = Column(Integer, ForeignKey('charging_locations.charging_location_id'), nullable=False)


class Pricing(Base):
    __tablename__ = 'pricing'

    pricing_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('booking.booking_id'), nullable=False)
    currency = Column(Text, nullable=True)
    total_value = Column(Float, nullable=True)
    price_per_khw = Column(Float, nullable=True)

class Activity(Base):
    __tablename__ = 'activity'

    car_owner_user_id = Column(Integer, nullable=True)
    charger_location_user_id = Column(Integer, nullable=True)
