import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.apis.v1.enpoints.user import router as user_router
from src.apis.v1.enpoints.charging_location import router as charging_location_router
from src.apis.v1.enpoints.car import router as car_router
from src.apis.v1.enpoints.booking import router as booking_router
from src.apis.v1.enpoints.notification import router as notification_router

from src.config.base import BaseConfig
from src.config.logging_config import setup_logging
from src.core.utils.error_middleware import LogErrorsMiddleware
from src.core.utils.middleware import RequestHeadersMiddleware

# Set up logging configuration
setup_logging()
logger = logging.getLogger(__name__)

settings = BaseConfig()

app = FastAPI(openapi_url="/v1/openapi.json",
              docs_url="/v1/docs",
              redoc_url="/v1/redoc",
              version="1.0.0",
              title=" Service",
              description=" Service",
              )

origins = [
    "http://localhost",
]

app.add_middleware(LogErrorsMiddleware)
app.add_middleware(RequestHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router, tags=["user_overview router"])
app.include_router(charging_location_router, tags=["charging_location router"])
app.include_router(car_router, tags=["car router"])
app.include_router(booking_router, tags=["booking router"])
app.include_router(notification_router, tags=["notification router"])



@app.get("/")
def index():
    return 'Hello'


if __name__ == '__main__':
    logger.info(settings.PORT)
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=False)
