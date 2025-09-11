from typing import List, Optional
from pydantic import BaseModel, Field

class ImportPublicChargersRequest(BaseModel):
    countries: List[str] = Field(default_factory=lambda: ["NL", "IR"])  # ISO codes
    max_results: int = 1000

class NearbyPublicChargersQuery(BaseModel):
    lat: float
    lon: float
    distance_km: float = 10.0

class BBoxPublicChargersQuery(BaseModel):
    north: float
    south: float
    east: float
    west: float

class PublicChargerOut(BaseModel):
    id: int
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str
    latitude: float
    longitude: float
    power_kw: Optional[float] = None
    connectors: Optional[str] = None
    operator: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
