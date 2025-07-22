from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette import status

from src.apis.v1.functionalities.charging_location.factory import get_charging_loc_service
from src.apis.v1.functionalities.charging_location.service import ChargingLocService
from src.apis.v1.schemas.charging_location import CreateChargingLocRequest, ChargingLocResponse, FindChargingLocRequest, \
    UpdateChargingLocRequest, FindNearbyChargingLocRequest
from src.core.utils.authentication import authenticate

router = APIRouter(dependencies=[Depends(authenticate)])


@router.post("/add-charging-location", status_code=status.HTTP_201_CREATED)
async def create_charging_loc(
    charging_loc_data: CreateChargingLocRequest = Body(...),
    charging_loc_svc: ChargingLocService = Depends(get_charging_loc_service)
):
    try:
        new_charging_loc = charging_loc_svc.create_charging_loc(charging_loc_data)
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

@router.post("/update-charging-location/{charging_location_id}")
async def update_charging_loc(
    charging_location_data: UpdateChargingLocRequest = Body(...),
    charging_location_id: int = Path(..., title="The Charging Location ID"),
    charging_location_svc: ChargingLocService = Depends(get_charging_loc_service)
):
    update_charging_loc = charging_location_svc.update_charging_loc(charging_location_data, charging_location_id)

@router.post("/find-nearby-charging-location", status_code=status.HTTP_201_CREATED)
async def find_nearby_charging_loc(
    charging_loc_data: FindNearbyChargingLocRequest = Body(...),
    charging_loc_svc: ChargingLocService = Depends(get_charging_loc_service)
):
    return charging_loc_svc.find_nearby_charging_locs(charging_loc_data)