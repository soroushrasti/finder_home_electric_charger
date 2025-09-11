from typing import List, Dict
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from src.apis.v1.functionalities.public_charger.factory import get_public_charger_service
from src.apis.v1.functionalities.public_charger.service import PublicChargerService
from src.apis.v1.schemas.public_charger import (
    ImportPublicChargersRequest,
    NearbyPublicChargersQuery,
    BBoxPublicChargersQuery,
    PublicChargerOut,
)

router = APIRouter()


@router.post("/public-chargers/import", status_code=status.HTTP_200_OK)
async def import_public_chargers(
    req: ImportPublicChargersRequest = Body(default=ImportPublicChargersRequest()),
    svc: PublicChargerService = Depends(get_public_charger_service),
) -> Dict[str, int]:
    try:
        return await svc.import_from_ocm(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {e}")


@router.post("/public-chargers/nearby", response_model=List[PublicChargerOut])
async def nearby_public_chargers(
    q: NearbyPublicChargersQuery = Body(...),
    svc: PublicChargerService = Depends(get_public_charger_service),
):
    try:
        items = svc.find_nearby(q)
        return items
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {e}")


@router.post("/public-chargers/bbox", response_model=List[PublicChargerOut])
async def bbox_public_chargers(
    q: BBoxPublicChargersQuery = Body(...),
    svc: PublicChargerService = Depends(get_public_charger_service),
):
    try:
        items = svc.find_in_bbox(q)
        return items
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {e}")

