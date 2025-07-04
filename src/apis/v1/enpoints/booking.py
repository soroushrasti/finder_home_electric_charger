from cmath import e
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from src.apis.v1.functionalities.booking.factory import get_booking_service
from src.apis.v1.functionalities.booking.service import BookingService
from src.apis.v1.schemas.booking import AddBookingRequest, CreateBookingRequest, FindBookingRequest, UpdateBookingRequest
from src.core.models import Booking
from starlette import status
from src.apis.v1.schemas.car import FindCarRequest

router = APIRouter()


@router.get("/bookings/{car_id}")
async def get_booking_by_car_id(
    car_id: int = Path(..., title="The user ID"),
    booking_svc: BookingService = Depends(get_booking_service),
):
    booking = booking_svc.get_bookings(car_id)
    if not booking:
        return []
    return booking

# @router.get_booking_by_charging_location_id("/bookings/{charging_location_id}")
# async def get_booking_by_charging_location_id(
#     charging_location_id: int = Path(..., title="The charging location ID"),
#     booking_svc: BookingService = Depends(get_booking_service),
# ):
#     booking = booking_svc.get_bookings_by_charging_location_id(charging_location_id)
#     if not booking:
#         return []
#     return booking

@router.post("/add-booking", status_code=status.HTTP_201_CREATED)
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
    booking_data: FindBookingRequest = Body(...),
    booking_svc: BookingService = Depends(get_booking_service)
):
    try:
        new_booking = booking_svc.find_booking(booking_data)
        return new_booking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error finding booking: {str(e)}"
        )

@router.post("/update-booking/{booking_id}")
async def update_booking(
    booking_data: UpdateBookingRequest = Body(...),
    booking_id: int = Path(..., title="The Booking ID"),
    booking_svc: BookingService = Depends(get_booking_service)
):
    update_booking = booking_svc.update_booking(booking_data, booking_id)
