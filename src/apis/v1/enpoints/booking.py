from fastapi import APIRouter, Body, Depends, HTTPException, Path
from src.apis.v1.functionalities.booking.factory import get_booking_service
from src.apis.v1.functionalities.booking.service import BookingService
from src.apis.v1.schemas.booking import CreateBookingRequest
from starlette import status
from src.apis.v1.schemas.car import FindCarRequest

router = APIRouter()


@router.get("/bookings/users/{user_id}")
async def get_booking_by_user_id(
    user_id: int = Path(..., title="The user ID"),
    booking_svc: BookingService = Depends(get_booking_service),
):
    booking = booking_svc.get_bookings(user_id)
    if not booking:
        return []
    return booking



@router.post("/booking", status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: CreateBookingRequest = Body(...),
    booking_svc: BookingService = Depends(get_booking_service)
):
    try:
        new_booking = booking_svc.create_booking(booking_data.dict())
        return new_booking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating booking: {str(e)}"
        )


@router.post("/find-booking", status_code=status.HTTP_200_OK)
async def find_booking(
    booking_data: FindCarRequest = Body(...),
    booking_svc: BookingService = Depends(get_booking_service)
):
    try:
        new_booking = booking_svc.find_booking(booking_data)
        return new_booking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating booking: {str(e)}"
        )
