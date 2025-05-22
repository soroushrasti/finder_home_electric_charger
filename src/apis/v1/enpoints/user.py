from typing import Optional
from fastapi import APIRouter, Depends, Body, Path, Query
from starlette import status

from src.apis.v1.functionalities.authentication import UserAuthService
from src.apis.v1.functionalities.user_mgmt.service import UserService
from src.apis.v1.functionalities.user_mgmt.factory import get_user_service

router = APIRouter(dependencies=[Depends(UserAuthService())])


@router.get("/users/{user_id}")
async def check_username(
        user_id: int = Path(..., title="The username to check"),
        user_svc: UserService = Depends(get_user_service)
    ):
    pass

