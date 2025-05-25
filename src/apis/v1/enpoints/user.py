from typing import Optional
from fastapi import APIRouter, Depends, Body, Path, Query, HTTPException, status
from starlette import status
from fastapi import  HTTPException, status
from src.apis.v1.functionalities.user.service import UserService
from src.apis.v1.functionalities.user.factory import get_user_service, UserServiceFactory
from src.apis.v1.schemas.user import CreateUserRequest
from src.core.utils.authentication import authenticate_user

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., title="The user ID"),
    token: str = Depends(authenticate_user),
    user_svc: UserService = Depends(get_user_service)
):
    user = user_svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUserRequest = Body(...),
   user_svc: UserService = Depends(get_user_service),
   token: str = Depends(authenticate_user),
):
    try:
        new_user = user_svc.create_user(user_data.dict())
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/user/login", status_code=status.HTTP_200_OK)
async def login_user(
    username: str = Query(..., title="The username"),
    password: str = Query(..., title="The password"),
    user_svc: UserService = Depends(get_user_service)
):
    try:
        user = user_svc.login_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "user": user}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error logging in: {str(e)}"
        )