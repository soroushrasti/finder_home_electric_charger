from pydantic_settings import BaseSettings
from pydantic import Field
import os

class BaseConfig( BaseSettings):
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8080)
    DEBUG: str = Field(default="True")
    TOKEN: str = Field(default="12345")
    EMAIL: str = Field(default="email")
    PASSWORD: str = Field(default="password")
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: str = Field(default="587")
    ACCOUNT_SID: str = Field(default="account_sid")
    ACCOUNT_TOKEN: str = Field(default="account_token")
    TWILIO_NUMBER: str = Field(default="twilio_number")
    DATABASE_URL: str = Field(default="sqlite:///database.db")

    model_config = {
        "env_file": None if os.getenv("RAILWAY_ENVIRONMENT") else ".env.base",
        "case_sensitive": False,
        "extra": "allow"
    }



settings = BaseConfig()
