from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette import status

from src.apis.v1.functionalities.charging_location.factory import get_charging_loc_service
from src.apis.v1.functionalities.charging_location.service import ChargingLocService
from src.apis.v1.schemas.charging_location import CreateChargingLocRequest,ChargingLocResponse

router = APIRouter()



@router.get("/charging_locations/users/{user_id}")
async def get_charging_loc(
    user_id: int = Path(..., title="The user ID"),
    charging_loc_svc: ChargingLocService = Depends(get_charging_loc_service)
):
    charging_locs = charging_loc_svc.get_charging_loc(user_id)
    return [ChargingLocResponse(**loc.__dict__).model_dump(by_alias=True) for loc in charging_locs]




@router.post("/charging_location", status_code=status.HTTP_201_CREATED)
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
