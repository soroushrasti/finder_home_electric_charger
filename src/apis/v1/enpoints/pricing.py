from fastapi import Body
from src.apis.v1.functionalities.pricing.service import PricingService
from src.apis.v1.schemas.pricing import CreatePricingRequest, FindPricingRequest
from starlette import status
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from src.apis.v1.functionalities.pricing.factory import get_pricing_service


router = APIRouter()


@router.post("/add-pricing", status_code=status.HTTP_201_CREATED)
async def create_pricing(
    pricing_data: CreatePricingRequest = Body(...),
    pricing_svc: PricingService = Depends(get_pricing_service)
):
    try:
        new_pricing= pricing_svc.create_pricing(pricing_data.dict())
        return new_pricing
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating pricing: {str(e)}"
        )

@router.post("/find-pricing", status_code=status.HTTP_200_OK)
async def find_pricing(
    pricing_data: FindPricingRequest = Body(...),
    pricing_svc: PricingService = Depends(get_pricing_service)
):
    try:
        new_pricing = pricing_svc.find_pricing(pricing_data)
        return new_pricing
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error finding pricing: {str(e)}"
        )
