from src.apis.v1.schemas.activity import FindActivityRequest
from src.core.models import Car, ChargingLocation, Pricing, Booking, User


class ActivityRepositoryAbstract:
    pass


class ActivityRepository(ActivityRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def calculate_total_pricing(self, find_activity_data: FindActivityRequest):
        query =self.db_session.query(Pricing.total_value).join(Booking, Booking.booking_id == Pricing.booking_id)

        if find_activity_data.car_owner_user_id:
            query = query.join(Car, Car.car_id ==  Booking.car_id).join(User, Car.user_id == User.user_id).filter(User.user_id == find_activity_data.car_owner_user_id)
        elif find_activity_data.charger_location_owner_user_id:
            query = query.join(ChargingLocation, ChargingLocation.charging_location_id ==  Booking.charging_location_id).join(User, ChargingLocation.user_id == User.user_id).filter(ChargingLocation.user_id == find_activity_data.charger_location_owner_user_id)

        return query.all()

    def calculate_number_bookings(self, find_activity_data: FindActivityRequest):
        query =self.db_session.query(Booking.booking_id)

        if find_activity_data.car_owner_user_id:
            query = query.join(Car, Car.car_id ==  Booking.car_id).join(User, Car.user_id == User.user_id).filter(User.user_id == find_activity_data.car_owner_user_id)
        elif find_activity_data.charger_location_owner_user_id:
            query = query.join(ChargingLocation, ChargingLocation.charging_location_id ==  Booking.charging_location_id).join(User, ChargingLocation.user_id == User.user_id).filter(ChargingLocation.user_id == find_activity_data.charger_location_owner_user_id)

        return query.all()

    def calculate_number_locations(self, find_activity_data: FindActivityRequest):
        query =self.db_session.query(ChargingLocation.charging_location_id).join(User, User.user_id == ChargingLocation.user_id)

        if find_activity_data.car_owner_user_id:
            query = query.filter(User.user_id == find_activity_data.car_owner_user_id)
        elif find_activity_data.charger_location_owner_user_id:
            query = query.filter(ChargingLocation.user_id == find_activity_data.charger_location_owner_user_id)

        return query.all()
