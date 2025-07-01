from src.core.models import Booking, ChargingLocation
from src.apis.v1.schemas.charging_location import FindChargingLocRequest


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

    def update_charging_loc(self, charging_loc_id: int, charging_loc_data: dict):
        # Logic to update an existing charging location in the database
        pass

    def delete_charging_loc(self, charging_loc_id: int):
        # Logic to delete a charging location from the database
        pass

    def find_charging_loc(self, find_charging_location_data: FindChargingLocRequest):
        query = self.db_session.query(ChargingLocation).join(Booking).filter(Booking.booking_id == ChargingLocation. booking_id)

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
