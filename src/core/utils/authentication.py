import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config.base import BaseConfig, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
basis_token = os.getenv("TOKEN")
def authenticate(token: str = Depends(oauth2_scheme)):
    return token
    if token != basis_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
