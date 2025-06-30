from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette import status

from src.apis.v1.functionalities.charging_location.factory import get_charging_loc_service
from src.apis.v1.functionalities.charging_location.service import ChargingLocService
from src.apis.v1.schemas.charging_location import CreateChargingLocRequest,ChargingLocResponse,FindChargingLocRequest

router = APIRouter()


@router.post("/add-charging-location", status_code=status.HTTP_201_CREATED)
async def create_charging_loc(
    charging_loc_data: CreateChargingLocRequest = Body(...),
    charging_loc_svc: ChargingLocService = Depends(get_charging_loc_service)
):
    try:
        new_charging_loc = charging_loc_svc.create_charging_loc(charging_loc_data.dict())
        return new_charging_loc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating charging loc: {str(e)}"
        )

@router.post("/find-charging-location", status_code=status.HTTP_201_CREATED)
async def find_charging_loc(
    charging_loc_data: FindChargingLocRequest = Body(...),
    charging_loc_svc: ChargingLocService = Depends(get_charging_loc_service)
):
    return charging_loc_svc.find_charging_locs(charging_loc_data)
