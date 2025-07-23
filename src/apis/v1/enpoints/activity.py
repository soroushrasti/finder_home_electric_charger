from fastapi import APIRouter, Body, Depends, HTTPException
from src.apis.v1.functionalities.activity.factory import get_activity_service
from src.apis.v1.functionalities.activity.service import ActivityService
from src.apis.v1.schemas.activity import FindActivityRequest
from starlette import status
from src.core.utils.authentication import authenticate

router = APIRouter(dependencies=[Depends(authenticate)])


@router.post("/get-activity", status_code=status.HTTP_200_OK)
async def find_activity(
    activity_data: FindActivityRequest = Body(...),
    activity_svc: ActivityService = Depends(get_activity_service)
):
    try:
        new_activity = activity_svc.find_activity(activity_data)
        return new_activity
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error finding activity: {str(e)}"
        )
