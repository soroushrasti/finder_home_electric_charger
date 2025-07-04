from itertools import count
import select
from requests import Session
from fastapi import Depends
from src.apis.v1.schemas.activity import FindActivityRequest
from src.config.database import create_session
from src.core.db_repository.activity import ActivityRepositoryAbstract, ActivityRepository
from src.core.models import Booking, ChargingLocation, Pricing

class ActivityService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo = activity_repo

    def find_activity(self, find_activity_data: FindActivityRequest):

       total_price = sum(self.activity_repo.calculate_total_pricing(find_activity_data))
       number_bookings = len(self.activity_repo.calculate_number_bookings(find_activity_data))
       number_locations = len(self.activity_repo.calculate_number_locations(find_activity_data))

       return {
            "total_price": total_price,
            "number_bookings": number_bookings,
            "number_locations": number_locations
        }
