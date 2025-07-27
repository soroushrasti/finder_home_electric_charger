from cmath import e
from datetime import datetime
from fastapi import HTTPException, Body, Depends
from sqlalchemy.sql.functions import func

from src.apis.v1.schemas.booking import FindBookingRequest, UpdateBookingRequest
from src.apis.v1.schemas.booking import FindBookingRequest
from src.core.models import Booking, User, ChargingLocation, Car, Pricing
from starlette import status
from sqlalchemy.orm import joinedload

class BookingRepositoryAbstract:
    pass


class BookingRepository(BookingRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_booking_by_id(self, car_id: int):
        return self.db_session.query(Booking).filter(Booking.car_id == car_id).all()

    # def get_booking_by_charging_location_id(self, charging_location_id: int):
    #     return self.db_session.query(Booking).filter(Booking.charging_location_id == charging_location_id).all()

    def create_booking(self, booking_data: dict):
        new_booking = Booking(**booking_data)
        new_booking.end_time = None
        new_booking.start_time = datetime.now()
        new_booking.status = "Success"
        self.db_session.add(new_booking)
        self.db_session.commit()
        return new_booking

    def update_booking(self, booking_id: int, booking_data: UpdateBookingRequest):
        booking: Booking = self.db_session.query(Booking).filter(Booking.booking_id == booking_id).first()

        if booking:
            self.pricing_calculate(booking, booking_data)
            if booking_data.car_id :
             booking.car_id = booking_data.car_id
            if booking_data.charging_location_id:
             booking.charging_location_id = booking_data.charging_location_id
            if booking_data.start_time:
             booking.start_time = booking_data.start_time
            if booking_data.end_time:
             booking.end_time = booking_data.end_time
            if booking_data.review_rate:
             booking.review_rate = booking_data.review_rate
            if booking_data.review_message:
             booking.review_message = booking_data.review_message
            if booking_data.status:
             booking.status = booking_data.status
            self.db_session.commit()
            return booking

        else:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error finding booking: {str(e)}"
            )


    def delete_booking(self, booking_id: int):
            # Logic to delete a car from the database
            pass

    def find_booking(self, find_booking_data: FindBookingRequest):
        query = (self.db_session.query(Booking)
                 .options(joinedload(Booking.car), joinedload(Booking.charging_location))
                 .join(Car).filter(Car.car_id == Booking.car_id).
                 join(ChargingLocation).filter(ChargingLocation.charging_location_id == Booking.charging_location_id))

        if find_booking_data.car_id:
            query = query.filter(Booking.car_id == find_booking_data.car_id)
        if find_booking_data.charging_location_id:
            query = query.filter(Booking.charging_location_id == find_booking_data.charging_location_id)
        if find_booking_data.review_rate:
            query = query.filter(Booking.review_rate == find_booking_data.review_rate)
        if find_booking_data.start_time:
            query = query.filter(Booking.start_time == find_booking_data.start_time)
        if find_booking_data.end_time:
            query = query.filter(Booking.end_time == find_booking_data.end_time)
        if find_booking_data.review_message:
            query = query.filter(func.lower(Booking.review_message) == find_booking_data.review_message.lower())
        if find_booking_data.status:
            query = query.filter(Booking.status == find_booking_data.status)
        if find_booking_data.charger_location_owner_user_id:
            query = query.filter(ChargingLocation.user_id == find_booking_data.charger_location_owner_user_id)
        if find_booking_data.car_owner_user_id:
            query = query.filter(Car.user_id == find_booking_data.car_owner_user_id)

        return query.all()

    def pricing_calculate (self, booking:Booking, booking_data: UpdateBookingRequest):
        charging_location: ChargingLocation = self.db_session.query(ChargingLocation).filter(ChargingLocation.charging_location_id == booking_data.charging_location_id).first()
        if not booking.end_time and booking_data.end_time:
            new_pricing = Pricing()
            price_per_hour = charging_location.price_per_hour
            new_pricing.booking_id = booking.booking_id
            new_pricing.currency = charging_location.currency
            new_pricing.total_value = (booking_data.end_time - booking_data.start_time) * price_per_hour
            new_pricing.price_per_kwh = None

            self.db_session.add(new_pricing)
            self.db_session.commit()
            return new_pricing

        return None