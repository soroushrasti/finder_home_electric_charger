from pydantic_settings import BaseSettings
from pydantic import Field
import os

class BaseConfig( BaseSettings):
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8080)
    DEBUG: str = Field(default="True")
    TOKEN: str = Field(default="your_token_here")
    EMAIL: str = Field(default="email")
    PASSWORD: str = Field(default="password")
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: str = Field(default="587")
    ACCOUNT_SID: str = Field(default="account_sid")
    ACCOUNT_TOKEN: str = Field(default="account_token")
    TWILIO_NUMBER: str = Field(default="twilio_number")
    DATABASE_URL: str = Field(default="sqlite:///database.db")
    # Email provider config
    EMAIL_PROVIDER: str = Field(default="smtp")  # options: smtp, sendgrid
    SENDGRID_API_KEY: str = Field(default="")
    SENDGRID_SENDER: str = Field(default="")
    EMAIL_ENABLED: bool = Field(default=True)
    EMAIL_STRICT: bool = Field(default=False)

    model_config = {
        "env_file": None,  # Disable .env file loading on Railway
        "case_sensitive": False,
        "extra": "allow"
    }



settings = BaseConfig()
