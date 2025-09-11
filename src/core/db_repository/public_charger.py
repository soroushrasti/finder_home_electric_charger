from typing import List, Optional
from math import radians, sin, cos, atan2, sqrt
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from src.core.models import PublicCharger


class PublicChargerRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_source_external(self, source: str, external_id: str) -> Optional[PublicCharger]:
        return (
            self.db.query(PublicCharger)
            .filter(PublicCharger.source == source, PublicCharger.external_id == external_id)
            .first()
        )

    def upsert_many(self, items: List[dict]) -> int:
        """Insert or update a list of public chargers. Returns count of upserts.
        items fields: source, external_id, name, address, city, country, latitude, longitude,
        power_kw, connectors, operator, is_active, last_seen
        """
        count = 0
        for it in items:
            existing = self.get_by_source_external(it["source"], it["external_id"])
            if existing:
                # Update selected fields
                for k in [
                    "name",
                    "address",
                    "city",
                    "country",
                    "latitude",
                    "longitude",
                    "power_kw",
                    "connectors",
                    "operator",
                    "is_active",
                    "last_seen",
                ]:
                    setattr(existing, k, it.get(k))
                count += 1
            else:
                obj = PublicCharger(**it)
                self.db.add(obj)
                count += 1
        self.db.commit()
        return count

    def find_within_bounds(self, north: float, south: float, east: float, west: float) -> List[PublicCharger]:
        lat_cond = and_(PublicCharger.latitude <= north, PublicCharger.latitude >= south)
        lon_cond = and_(PublicCharger.longitude <= east, PublicCharger.longitude >= west)
        return (
            self.db.query(PublicCharger)
            .filter(lat_cond)
            .filter(lon_cond)
            .all()
        )

    def find_nearby(self, lat: float, lon: float, distance_km: float = 10.0, limit: int = 500) -> List[PublicCharger]:
        # Rough prefilter by bounding box to reduce Python haversine checks
        lat_delta = distance_km / 111.0
        lon_delta = distance_km / (111.0 * max(0.1, cos(radians(lat))))
        candidates = self.find_within_bounds(lat + lat_delta, lat - lat_delta, lon + lon_delta, lon - lon_delta)
        result = []
        for c in candidates:
            if self._haversine(lat, lon, float(c.latitude), float(c.longitude)) <= distance_km:
                result.append(c)
                if len(result) >= limit:
                    break
        return result

    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

