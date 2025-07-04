from fastapi import HTTPException

from src.core.models import Booking, ChargingLocation, User
from src.apis.v1.schemas.charging_location import FindChargingLocRequest
from starlette import status
from cmath import e


class ChargingLocRepositoryAbstract:
    pass

class ChargingLocRepository(ChargingLocRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_charging_loc_by_id(self, user_id: int):
        return self.db_session.query(ChargingLocation).filter(ChargingLocation.user_id == user_id).all()

    def create_charging_loc(self, charging_loc_data: dict):
        new_charging_loc = ChargingLocation(**charging_loc_data)
        self.db_session.add(new_charging_loc)
        self.db_session.commit()
        return new_charging_loc

    def update_charging_loc(self, charging_location_id: int, charging_location_data: dict):
        # Logic to update an existing charging location in the database
        query = self.db_session.query(ChargingLocation).filter(
            ChargingLocation.charging_location_id == charging_location_id).first()
        if query:
            if charging_location_data.user_id:
                query.user_id = charging_location_data.user_id
            if charging_location_data.post_code:
                query.post_code = charging_location_data.post_code
            if charging_location_data.alley:
                query.alley = charging_location_data.alley
            if charging_location_data.street:
                query.street = charging_location_data.street
            if charging_location_data.home_phone_number:
                query.home_phone_number = charging_location_data.home_phone_number
            if charging_location_data.city:
                query.city = charging_location_data.city
            if charging_location_data.fast_charging:
                query.fast_charging = charging_location_data.fast_charging
            if charging_location_data.name:
                query.name = charging_location_data.name
            if charging_location_data.price_per_hour:
                query.price_per_hour = charging_location_data.price_per_hour
            if charging_location_data.power_output:
                query.power_output = charging_location_data.power_output
            if charging_location_data.description:
                query.description = charging_location_data.description
            self.db_session.commit()
            return query

        else:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error updating charging location{(e)}"
            )

    def delete_charging_loc(self, charging_loc_id: int):
        # Logic to delete a charging location from the database
        pass

    def find_charging_loc(self, find_charging_location_data: FindChargingLocRequest):
        query = self.db_session.query(ChargingLocation).join(User).filter(User.user_id == ChargingLocation. user_id)

        if find_charging_location_data.post_code:
            query = query.filter(ChargingLocation.post_code == find_charging_location_data.post_code)
        if find_charging_location_data.alley:
            query = query.filter(ChargingLocation.alley == find_charging_location_data.alley)
        if find_charging_location_data.street:
            query = query.filter(ChargingLocation.street == find_charging_location_data.street)
        if find_charging_location_data.home_phone_number:
            query = query.filter(ChargingLocation.home_phone_number == find_charging_location_data.home_phone_number)
        if find_charging_location_data.city:
            query = query.filter(ChargingLocation.city == find_charging_location_data.city)
        if find_charging_location_data.fast_charging:
            query = query.filter(ChargingLocation.fast_charging == find_charging_location_data.fast_charging)
        if find_charging_location_data.user_id:
            query = query.filter(ChargingLocation.user_id == find_charging_location_data.user_id)

        return query.all()

    def get_booking_by_charging_location_id(self, charging_location_id: int):
        return self.db_session.query(Booking).filter(Booking.charging_location_id == charging_location_id).filter(Booking.end_time== None).first()


