from src.core.db_repository.charging_location import ChargingLocRepositoryAbstract, ChargingLocRepository


class ChargingLocService:
    def __init__(self, charging_loc_repo: ChargingLocRepository):
        self.charging_loc_repo = charging_loc_repo

    def get_charging_loc(self, user_id: int):
        return self.charging_loc_repo.get_charging_loc_by_id(user_id)

    def create_charging_loc(self, charging_loc_data: dict):
        return self.charging_loc_repo.create_charging_loc(charging_loc_data)

    def find_charging_locs(self, charging_loc_data):
        locations= self.charging_loc_repo.find_charging_loc(charging_loc_data)
        for location in locations:
            location.is_available = True
        return locations
