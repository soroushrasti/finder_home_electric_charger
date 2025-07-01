from itertools import count
import select
from requests import Session
from fastapi import Depends
from src.apis.v1.functionalities.activity.factory import ActivityServiceFactory
from src.apis.v1.schemas.activity import FindActivityRequest
from src.config.database import create_session
from src.core.db_repository.activity import ActivityRepositoryAbstract, ActivityRepository
from src.core.models import Booking, ChargingLocation, Pricing


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo = activity_repo

    def find_activity(self, find_activity_data: FindActivityRequest):
        activities = self.activity_repo.find_activity(find_activity_data)

        for activity in activities:

        # total price
           total_price = activity.sum(Pricing.total_value)
        # number of bookings
           number_bookings = activity.count(Booking.booking_id)
        # number of locations
           number_locations = activity.count(ChargingLocation.charging_location_id)

        return activities

def get_activity_service(
        db: Session = Depends(create_session)
        ):
    repo = ActivityRepository(db_session=db)
    factory = ActivityServiceFactory(repo=repo)
    return factory.get_service()
