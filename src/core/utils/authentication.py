from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config.base import BaseConfig, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate(token: str = Depends(oauth2_scheme)):
    if token != BaseConfig().TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
