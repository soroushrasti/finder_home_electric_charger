from fastapi import APIRouter

from src.apis.v1.enpoints.pricing import create_pricing
from src.apis.v1.schemas.booking import FindBookingRequest
from src.apis.v1.schemas.booking import FindBookingRequest
from src.core.db_repository.booking import BookingRepository
from src.core.db_repository.booking import BookingRepositoryAbstract, BookingRepository
from src.core.models import ChargingLocation, Pricing


class BookingService:
    def __init__(self, booking_repo: BookingRepository):
        self.booking_repo = booking_repo

    def get_bookings(self, car_id: int):
        return self.booking_repo.get_booking_by_id(car_id)

    # def get_bookings_by_charging_location_id(self, charging_location_id: int):
    #     return self.booking_repo.get_booking_by_charging_location_id(charging_location_id)

    # Add to src/apis/v1/functionalities/user/service.py
    def create_booking(self, booking_data: dict):
        return self.booking_repo.create_booking(booking_data)

    def find_booking(self, find_booking_data: FindBookingRequest):
        return self.booking_repo.find_booking(find_booking_data)

    def update_booking(self, booking_data: dict, booking_id: int):
        self.booking_repo.pricing_calculate(booking_id, booking_data)
        return self.booking_repo.update_booking(booking_id , booking_data)







