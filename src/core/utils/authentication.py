from fastapi import Header, HTTPException, status
import os

from src.config.base import BaseConfig

config = BaseConfig()


def authenticate(x_api_token: str = Header(None)):

    if x_api_token != config.TOKEN:
        print(x_api_token)
        print(config.TOKEN)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return x_api_token