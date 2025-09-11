from typing import List

from fastapi import HTTPException
from math import radians, sin, cos, atan2, sqrt

from sqlalchemy.sql.functions import func

from src.core.models import Booking, ChargingLocation, User, Review
from src.apis.v1.schemas.charging_location import FindChargingLocRequest, FindNearbyChargingLocRequest, \
    CreateChargingLocRequest
from starlette import status
from cmath import e


class ChargingLocRepositoryAbstract:
    pass

class ChargingLocRepository(ChargingLocRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_charging_loc_by_id(self, user_id: int):
        return self.db_session.query(ChargingLocation).filter(ChargingLocation.user_id == user_id).all()

    def create_charging_loc(self, charging_loc_data: CreateChargingLocRequest):
        new_charging_loc = ChargingLocation(**charging_loc_data.dict())
        self.db_session.add(new_charging_loc)
        self.db_session.commit()
        return new_charging_loc

    def update_charging_loc(self, charging_location_id: int, charging_location_data: dict):
        # Logic to update an existing charging location in the database
        query: ChargingLocation = self.db_session.query(ChargingLocation).filter(
            ChargingLocation.charging_location_id == charging_location_id).first()
        if query:
            if charging_location_data.user_id:
                query.user_id = charging_location_data.user_id
            if charging_location_data.post_code:
                query.post_code = charging_location_data.post_code
            if charging_location_data.alley:
                query.alley = charging_location_data.alley
            if charging_location_data.street:
                query.street = charging_location_data.street
            if charging_location_data.home_phone_number:
                query.home_phone_number = charging_location_data.home_phone_number
            if charging_location_data.city:
                query.city = charging_location_data.city
            if charging_location_data.fast_charging:
                query.fast_charging = charging_location_data.fast_charging
            if charging_location_data.name:
                query.name = charging_location_data.name
            if charging_location_data.price_per_hour:
                query.price_per_hour = charging_location_data.price_per_hour
            if charging_location_data.power_output:
                query.power_output = charging_location_data.power_output
            if charging_location_data.description:
                query.description = charging_location_data.description
            if charging_location_data.currency:
                query.currency = charging_location_data.currency
            if charging_location_data.latitude:
                query.latitude = charging_location_data.latitude
            if charging_location_data.longitude:
                query.longitude = charging_location_data.longitude
            if charging_location_data.country:
                query.country = charging_location_data.country

            self.db_session.commit()
            return query

        else:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error updating charging location{(e)}"
            )

    def delete_charging_loc(self, charging_loc_id: int):
        # Logic to delete a charging location from the database
        self.db.query(ChargingLocation).filter(ChargingLocation.charging_location_id == charging_loc_id).delete()
        self.db.commit()

    def find_charging_loc(self, find_charging_location_data: FindChargingLocRequest):
        query = self.db_session.query(ChargingLocation).join(User, User.user_id == ChargingLocation.user_id)

        if find_charging_location_data.post_code:
            query = query.filter(func.lower(ChargingLocation.post_code) == find_charging_location_data.post_code.lower())
        if find_charging_location_data.alley:
            query = query.filter(func.lower(ChargingLocation.alley) == find_charging_location_data.alley.lower())
        if find_charging_location_data.street:
            query = query.filter(func.lower(ChargingLocation.street) == find_charging_location_data.street.lower())
        if find_charging_location_data.home_phone_number:
            query = query.filter(func.lower(ChargingLocation.home_phone_number) == find_charging_location_data.home_phone_number.lower())
        if find_charging_location_data.city:
            query = query.filter(func.lower(ChargingLocation.city) == find_charging_location_data.city.lower())
        if find_charging_location_data.fast_charging:
            query = query.filter(ChargingLocation.fast_charging == find_charging_location_data.fast_charging)
        if find_charging_location_data.user_id:
            query = query.filter(ChargingLocation.user_id == find_charging_location_data.user_id)
        if find_charging_location_data.name:
            query = query.filter(func.lower(ChargingLocation.name) == find_charging_location_data.name.lower())
        if find_charging_location_data.description:
            query = query.filter(func.lower(ChargingLocation.description) == find_charging_location_data.description.lower())
        if find_charging_location_data.currency:
            query = query.filter(func.lower(ChargingLocation.currency) == find_charging_location_data.currency.lower())
        if find_charging_location_data.country:
            query = query.filter(func.lower(ChargingLocation.country) == find_charging_location_data.country.lower())
        if find_charging_location_data.price_per_hour:
            query = query.filter(ChargingLocation.price_per_hour == find_charging_location_data.price_per_hour)
        if find_charging_location_data.power_output:
            query = query.filter(ChargingLocation.power_output == find_charging_location_data.power_output)
        if find_charging_location_data.latitude:
            query = query.filter(ChargingLocation.latitude == find_charging_location_data.latitude)
        if find_charging_location_data.longitude:
            query = query.filter(ChargingLocation.longitude == find_charging_location_data.longitude)

        return query.all()

    def get_non_ended_booking_by_charging_location_id(self, charging_location_id: int):
        return self.db_session.query(Booking).filter(Booking.charging_location_id == charging_location_id).filter(Booking.end_time== None).first()

    def find_nearby_charging_loc(self, charging_loc_data: FindNearbyChargingLocRequest):
        locations: List[ChargingLocation] = self.db_session.query(ChargingLocation).all()
        filter_locations = []
        for location in locations:
            if  charging_loc_data.latitude and charging_loc_data.longitude and location.latitude and location.longitude:
                if self.haversine_daistance(latitude1=charging_loc_data.latitude, longitude1=charging_loc_data.longitude,
                                            latitude2=location.latitude, longitude2=location.longitude)<= charging_loc_data.distance:
                    filter_locations.append(location)
        return filter_locations

    def haversine_daistance(self, latitude1: float, longitude1: float, latitude2: float, longitude2: float):
            radios = 6371.0
            latitude1, longitude1, latitude2, longitude2 = map(radians,[latitude1, longitude1, latitude2, longitude2])

            dlat = latitude2 - latitude1
            dlon = longitude2 - longitude1

            a = sin(dlat / 2) ** 2 + cos(latitude1) ** cos(latitude2) ** sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = radios * c
            return distance


    def review_statistics(self):
        query= self.db_session.query(ChargingLocation.charging_location_id, func.avg(Review.review_rate), func.count(Review.review_rate)).join(Review).group_by(ChargingLocation.charging_location_id)
        return query.all()

    def find_within_bounds(self, north: float, south: float, east: float, west: float) -> List[ChargingLocation]:
        return (
            self.db_session.query(ChargingLocation)
            .filter(ChargingLocation.latitude >= south, ChargingLocation.latitude <= north)
            .filter(ChargingLocation.longitude >= west, ChargingLocation.longitude <= east)
            .all()
        )
