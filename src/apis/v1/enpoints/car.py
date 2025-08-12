from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette import status

from src.apis.v1.functionalities.car.factory import get_car_service
from src.apis.v1.functionalities.car.service import CarService
from src.apis.v1.schemas.car import CreateCarRequest, FindCarRequest, UpdateCarRequest
from src.core.utils.authentication import authenticate

router = APIRouter(dependencies=[Depends(authenticate)])


@router.get("/cars/{user_id}")
async def get_car_by_user_id(
    user_id: int = Path(..., title="The user ID"),
    car_svc: CarService = Depends(get_car_service),
):
    car = car_svc.get_cars(user_id)
    if not car:
        raise HTTPException(status_code=404, detail="car not found")
    return car


@router.post("/add-car", status_code=status.HTTP_201_CREATED)
async def create_car(
    car_data: CreateCarRequest = Body(...),
    car_svc: CarService = Depends(get_car_service)
):
    try:
        new_car = car_svc.create_car(car_data.dict())
        return new_car
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating car: {str(e)}"
        )


@router.post("/find-car", status_code=status.HTTP_200_OK)
async def find_car(
    car_data: FindCarRequest = Body(...),
    car_svc: CarService = Depends(get_car_service)
):
    try:
        new_car = car_svc.find_car(car_data)
        return new_car
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error finding car: {str(e)}"
        )


@router.post("/update-car/{car_id}")
async def update_car(
    car_data: UpdateCarRequest = Body(...),
        car_id: int = Path(..., title="The Car ID"),
        car_svc: CarService = Depends(get_car_service)
):
    updated_car = car_svc.update_car(car_data=car_data, car_id=car_id)
    return updated_car
