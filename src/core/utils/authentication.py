from fastapi import Header, HTTPException, status
import os

basis_token = os.getenv("TOKEN")


def authenticate(x_api_token: str = Header(None)):
    if not x_api_token:
        return "disabled"  # For testing

    if x_api_token != basis_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return x_api_token