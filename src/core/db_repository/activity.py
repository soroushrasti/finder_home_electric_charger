from src.apis.v1.schemas.activity import FindActivityRequest
from src.core.models import Activity, Car, ChargingLocation, Pricing, Booking, User


class ActivityRepositoryAbstract:
    pass


class ActivityRepository(ActivityRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def calculate_total_pricing(self, find_activity_data: FindActivityRequest):
        query =self.db_session.querty(Pricing.total_value).join(Booking, Booking.booking_id == Pricing.booking_id).\
            join(User, User.user_id == Booking.user_id)

        if find_activity_data.car_owner_user_id:
            query = query.filter(User.user_id == find_activity_data.car_owner_user_id)
        elif find_activity_data.charger_location_owner_user_id:
            query = query.filter(ChargingLocation.user_id == find_activity_data.charger_location_owner_user_id)

        return query.all()

