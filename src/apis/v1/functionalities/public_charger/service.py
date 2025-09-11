from typing import List, Dict
import json
from datetime import datetime, UTC
import logging
import httpx

from src.config.base import settings
from src.core.db_repository.public_charger import PublicChargerRepository
from src.apis.v1.schemas.public_charger import ImportPublicChargersRequest, NearbyPublicChargersQuery, BBoxPublicChargersQuery

logger = logging.getLogger(__name__)


class PublicChargerService:
    def __init__(self, repo: PublicChargerRepository):
        self.repo = repo

    async def import_from_ocm(self, req: ImportPublicChargersRequest) -> Dict[str, int]:
        """Fetch chargers from OpenChargeMap for given countries and upsert into DB."""
        base = settings.OCM_API_BASE.rstrip("/")
        key = settings.OCM_API_KEY
        totals: Dict[str, int] = {}
        headers = {
            "Accept": "application/json",
            # A descriptive UA helps with OCM rate limiting policies
            "User-Agent": "BridgeEnergy/1.0 (+https://charge-bridge.com)",
        }
        if key:
            headers["X-API-Key"] = key
        params_common = {
            "output": "json",
            "maxresults": req.max_results,
        }
        async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
            for cc in req.countries:
                params = dict(params_common)
                params["countrycode"] = cc
                if key:
                    params["key"] = key  # also include as query param per OCM docs
                logger.info("Fetching OCM data for country=%s", cc)
                r = await client.get(base, params=params)
                if r.status_code == 403:
                    raise httpx.HTTPStatusError(
                        "OpenChargeMap returned 403 Forbidden. Set a valid OCM_API_KEY.", request=r.request, response=r
                    )
                r.raise_for_status()
                data = r.json()
                items = []
                for poi in data:
                    try:
                        addr_info = poi.get("AddressInfo") or {}
                        st = poi.get("StatusType") or {}
                        op = poi.get("OperatorInfo") or {}
                        connections = poi.get("Connections") or []
                        max_kw = None
                        connector_types = []
                        for c in connections:
                            kw = c.get("PowerKW") or (c.get("Voltage") and c.get("Amps") and (c.get("Voltage") * c.get("Amps") / 1000.0))
                            if isinstance(kw, (int, float)):
                                max_kw = max(kw if max_kw is None else max_kw, kw)
                            ctype = (c.get("ConnectionType") or {}).get("Title")
                            if ctype:
                                connector_types.append(ctype)
                        item = {
                            "source": "openchargemap",
                            "external_id": str(poi.get("ID")),
                            "name": addr_info.get("Title"),
                            "address": addr_info.get("AddressLine1"),
                            "city": addr_info.get("Town"),
                            "country": (addr_info.get("Country") or {}).get("ISOCode") or cc,
                            "latitude": float(addr_info.get("Latitude")),
                            "longitude": float(addr_info.get("Longitude")),
                            "power_kw": float(max_kw) if max_kw is not None else None,
                            "connectors": json.dumps(sorted(set(connector_types))) if connector_types else None,
                            "operator": op.get("Title"),
                            "is_active": bool(st.get("IsOperational")) if st else None,
                            "last_seen": datetime.now(UTC),
                        }
                        items.append(item)
                    except Exception as e:
                        logger.warning("Skipping malformed OCM record: %s", e)
                        continue
                upserted = self.repo.upsert_many(items)
                totals[cc] = upserted
                logger.info("Upserted %s OCM chargers for %s", upserted, cc)
        return totals

    def find_nearby(self, q: NearbyPublicChargersQuery):
        return self.repo.find_nearby(q.lat, q.lon, q.distance_km)

    def find_in_bbox(self, q: BBoxPublicChargersQuery):
        return self.repo.find_within_bounds(q.north, q.south, q.east, q.west)
