from starlette import status
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from src.apis.v1.functionalities.notification.factory import get_notification_service
from src.apis.v1.functionalities.notification.service import NotificationService
from src.apis.v1.schemas.notification import CreateNotificationRequest, FindNotificationRequest


router = APIRouter()


@router.get("/bookings/{booking_id}")
async def get_notification_by_booking_id(
    booking_id: int = Path(..., title="The Booking ID"),
    notification_svc: NotificationService = Depends(get_notification_service),
):
    notification = notification_svc.get_notifications(booking_id)
    if not notification:
        return []
    return notification

@router.post("/notification", status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: CreateNotificationRequest = Body(...),
    notification_svc: NotificationService = Depends(get_notification_service)
):
    try:
        new_notification = notification_svc.create_notification(notification_data.dict())
        return new_notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating notification: {str(e)}"
        )

@router.post("/find-notification", status_code=status.HTTP_200_OK)
async def find_notification(
    notification_data: FindNotificationRequest = Body(...),
    notification_svc: NotificationService = Depends(get_notification_service)
):
    try:
        new_notification = notification_svc.find_notification(notification_data)
        return new_notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating notification: {str(e)}"
        )
