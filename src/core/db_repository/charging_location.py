from src.core.models import ChargingLocation


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
