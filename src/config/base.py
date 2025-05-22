from pydantic_settings import BaseSettings
from pydantic import Field

class BaseConfig( BaseSettings):
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8080)
    DEBUG: str = Field(default="True")

    class Config:
        env_file = ".env.base"


settings = BaseConfig()
