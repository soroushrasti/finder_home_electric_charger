from typing import List, Optional

from src.core.db_repository.charging_location import ChargingLocRepositoryAbstract, ChargingLocRepository
from src.core.models import Booking, ChargingLocation


class ChargingLocService:
    def __init__(self, charging_loc_repo: ChargingLocRepository):
        self.charging_loc_repo = charging_loc_repo

    def get_charging_loc(self, user_id: int):
        return self.charging_loc_repo.get_charging_loc_by_id(user_id)

    def create_charging_loc(self, charging_loc_data: dict):
        return self.charging_loc_repo.create_charging_loc(charging_loc_data)

    def find_charging_locs(self, charging_loc_data):
        locations : List[ChargingLocation]= self.charging_loc_repo.find_charging_loc(charging_loc_data)

        for location in locations:
            # if we have a booking and it has not ended, we set is_available to False
            booking: Optional[Booking] = self.charging_loc_repo.get_booking_by_charging_location_id(location.charging_location_id)
            if booking:
                location.is_available = False
            else:
                location.is_available = True

        return locations
