from typing import List, Optional

from src.apis.v1.schemas.charging_location import FindNearbyChargingLocRequest, CreateChargingLocRequest
from src.core.db_repository.charging_location import ChargingLocRepositoryAbstract, ChargingLocRepository
from src.core.models import Booking, ChargingLocation, Review


class ChargingLocService:
    def __init__(self, charging_loc_repo: ChargingLocRepository):
        self.charging_loc_repo = charging_loc_repo

    def get_charging_loc(self, user_id: int):
        return self.charging_loc_repo.get_charging_loc_by_id(user_id)

    def create_charging_loc(self, charging_loc_data: CreateChargingLocRequest):
        return self.charging_loc_repo.create_charging_loc(charging_loc_data)

    def find_charging_locs(self, charging_loc_data):
        locations : List[ChargingLocation]= self.charging_loc_repo.find_charging_loc(charging_loc_data)
        records = self.charging_loc_repo.review_statistics()

        for location in locations:
            # if we have a booking and it has not ended, we set is_available to False
            booking: Optional[Booking] = self.charging_loc_repo.get_non_ended_booking_by_charging_location_id(location.charging_location_id)
            if booking:
                location.is_available = False
            else:
                location.is_available = True

            for id, avg, count in records:
                if id == location.charging_location_id:
                    location.review_average = avg
                    location.review_number = count

        return locations

    def update_charging_loc(self, charging_location_data: dict, charging_location_id: int, ):
         return self.charging_loc_repo.update_charging_loc(charging_location_id , charging_location_data)

    def find_nearby_charging_locs(self, charging_loc_data: FindNearbyChargingLocRequest):
        locations : List[ChargingLocation]= self.charging_loc_repo.find_nearby_charging_loc(charging_loc_data)

        for location in locations:
            # if we have a booking and it has not ended, we set is_available to False
            booking: Optional[Booking] = self.charging_loc_repo.get_non_ended_booking_by_charging_location_id(
                location.charging_location_id)
            if booking:
                location.is_available = False
            else:
                location.is_available = True
        return locations

    def delete_charging_loc(self, charging_location_id: int, ):
         return self.charging_loc_repo.delete_charging_loc(charging_location_id)
