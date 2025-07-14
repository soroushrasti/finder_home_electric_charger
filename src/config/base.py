from pydantic_settings import BaseSettings
from pydantic import Field

class BaseConfig( BaseSettings):
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8080)
    DEBUG: str = Field(default="True")
    TOKEN: str = Field(default="12345")
    EMAIL: str = Field(default="")
    PASSWORD: str = Field(default="")
    SMTP_SERVER: str = Field(default="")
    SMTP_PORT: str = Field(default="")
    ACCOUNT_SID: str = Field(default="account_sid")
    ACCOUNT_TOKEN: str = Field(default="account_token")
    TWILIO_NUMBER: str = Field(default="twilio_number")

    class Config:
        env_file = ".env.base"


settings = BaseConfig()
