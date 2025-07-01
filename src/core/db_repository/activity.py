from src.apis.v1.schemas.activity import FindActivityRequest
from src.core.models import Activity, Car, ChargingLocation


class ActivityRepositoryAbstract:
    pass


class ActivityRepository(ActivityRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def find_activity(self, find_activity_data: FindActivityRequest):
        query = (self.db_session.query(Activity).join(Car).filter(Car.car_id == Activity.car_id).
                 join(ChargingLocation).filter(ChargingLocation.charging_location_id ==Activity.charging_location_id))

        if find_activity_data.charger_location_owner_user_id:
            query = query.filter(ChargingLocation.user_id == find_activity_data.charger_location_owner_user_id)
        if find_activity_data.car_owner_user_id:
            query = query.filter(Car.user_id == find_activity_data.car_owner_user_id)

        return query.all()
