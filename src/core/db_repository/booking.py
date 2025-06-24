from src.apis.v1.schemas.booking import FindBookingRequest
from src.core.models import Booking


class BookingRepositoryAbstract:
    pass


class BookingRepository(BookingRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_booking_by_id(self, user_id: int):
        return self.db_session.query(Booking).filter(Booking.user_id == user_id).all()

    def create_booking(self, booking_data: dict):
        new_booking = Booking(**booking_data)
        self.db_session.add(new_booking)
        self.db_session.commit()
        return new_booking

    def update_booking(self, booking_id: int, booking_data: dict):
        # Logic to update an existing car in the database
        pass

    def delete_booking(self, booking_id: int):
        # Logic to delete a car from the database
        pass

    def find_booking(self, find_booking_data: FindBookingRequest):
        query = self.db_session.query(Booking)

        if find_booking_data.user_id:
            query = query.filter(Booking.user_id == find_booking_data.user_id)
        if find_booking_data.charging_location_id:
            query = query.filter(Booking.user_id == find_booking_data.charging_location_id)
        if find_booking_data.review_rate:
            query = query.filter(Booking.user_id == find_booking_data.review_rate)
        if find_booking_data.start_time:
            query = query.filter(Booking.user_id == find_booking_data.start_time)
        if find_booking_data.end_time:
            query = query.filter(Booking.user_id == find_booking_data.end_time)
        if find_booking_data.review_message:
            query = query.filter(Booking.user_id == find_booking_data.review_message)

        return query.all()
