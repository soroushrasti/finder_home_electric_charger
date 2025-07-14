from cmath import e
from datetime import datetime
from fastapi import HTTPException
from src.apis.v1.enpoints import booking
from src.apis.v1.enpoints.pricing import create_pricing
from src.apis.v1.schemas.booking import FindBookingRequest
from src.core.models import Booking, User, ChargingLocation, Car, Pricing
from starlette import status


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

    def update_booking(self, booking_id: int, booking_data: dict):
        query = self.db_session.query(Booking).filter(Booking.booking_id == booking_id).first()

        if query:
            if booking_data.car_id :
             query.car_id = booking_data.car_id
            if booking_data.charging_location_id:
             query.charging_location_id = booking_data.charging_location_id
            if booking_data.start_time:
             query.start_time = booking_data.start_time
            if booking_data.end_time:
             query.end_time = booking_data.end_time
            if booking_data.review_rate:
             query.review_rate = booking_data.review_rate
            if booking_data.review_message:
             query.review_message = booking_data.review_message
            if booking_data.status:
             query.status = booking_data.status
            self.db_session.commit()
            return query

        else:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error finding booking: {str(e)}"
            )


    def delete_booking(self, booking_id: int):
            # Logic to delete a car from the database
            pass

    def find_booking(self, find_booking_data: FindBookingRequest):
        query = (self.db_session.query(Booking).join(Car).filter(Car.car_id == Booking.car_id).
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
            query = query.filter(Booking.review_message == find_booking_data.review_message)
        if find_booking_data.status:
            query = query.filter(Booking.status == find_booking_data.status)
        if find_booking_data.charger_location_owner_user_id:
            query = query.filter(ChargingLocation.user_id == find_booking_data.charger_location_owner_user_id)
        if find_booking_data.car_owner_user_id:
            query = query.filter(Car.user_id == find_booking_data.car_owner_user_id)

        return query.all()

    def pricing_calculate (self, booking_id:int, booking_data: dict):
        user = self.db_session.query(ChargingLocation).filter(ChargingLocation.charging_location_id == booking_data.charging_location_id).first()
        query = self.db_session.query(Booking).filter(Booking.booking_id == booking_id).first()
        new_pricing = Pricing()
        if query.end_time:
            price_per_hour = user.price_per_hour
            new_pricing.booking_id = booking_id
            new_pricing.currency = user.currency
            new_pricing.total_value = (booking_data.end_time - booking_data.start_time) * price_per_hour
            new_pricing.price_per_kwh = None
            create_pricing(new_pricing)

        return new_pricing