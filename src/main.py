import logging
import subprocess
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.apis.v1.enpoints.user import router as user_router
from src.apis.v1.enpoints.charging_location import router as charging_location_router
from src.apis.v1.enpoints.car import router as car_router
from src.apis.v1.enpoints.booking import router as booking_router
from src.apis.v1.enpoints.notification import router as notification_router
from src.apis.v1.enpoints.pricing import router as pricing_router
from src.apis.v1.enpoints.activity import router as activity_router

from src.config.base import BaseConfig
from src.config.logging_config import setup_logging
from src.core.utils.error_middleware import LogErrorsMiddleware
from src.core.utils.middleware import RequestHeadersMiddleware, LoggingMiddleware

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
app.add_middleware(LoggingMiddleware)
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
app.include_router(pricing_router, tags=["pricing router"])
app.include_router(activity_router, tags=["activity router"])


def run_migrations():
    logger.info("=== Railway Environment Debug ===")

    # Check all Railway-specific environment variables
    railway_vars = {k: v for k, v in os.environ.items() if 'RAILWAY' in k.upper()}
    logger.info(f"Railway env vars: {railway_vars}")

    db_url = None
    for var in possible_db_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"Found {var}: {value[:50]}...")
            db_url = value
            break

    if not db_url:
        logger.warning("No Railway database URL found, using default SQLite")
        db_url = "sqlite:///database.db"

    logger.info(f"Using DATABASE_URL: {db_url[:50]}...")
    logger.info("=== End Railway Debug ===")

    if db_url and "postgresql" in db_url:
        settings.DATABASE_URL = db_url

    logger.info("=== Environment Debug ===")
    logger.info(f"RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT', 'Not set')}")
    logger.info(f"DATABASE_URL from env: {os.getenv('DATABASE_URL', 'Not set')}")
    logger.info(f"BaseConfig DATABASE_URL: {settings.DATABASE_URL}")
    logger.info("=== End Debug ===")
    db_url = os.getenv("DATABASE_URL") or settings.DATABASE_URL

    logger.info(f"Found DATABASE_URL: {db_url[:30]}...")

    # Create database file if it doesn't exist
    if db_url.startswith("sqlite:///"):
        db_file_path = db_url.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_file_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        # Create empty database file
        if not os.path.exists(db_file_path):
            open(db_file_path, 'a').close()

    try:
        from alembic.config import Config
        from alembic import command
        import traceback

        logger.info(f"Running database migrations with URL: {db_url[:20]}...")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up from src/ to project root

        alembic_ini_path = os.path.join(project_root, "alembic.ini")
        alembic_dir_path = os.path.join(project_root, "alembic")

        # Check if alembic.ini exists
        if not os.path.exists(alembic_ini_path):
            logger.error(f"alembic.ini not found at: {alembic_ini_path}")
            logger.error(f"Current working directory: {os.getcwd()}")
            logger.error(f"Project root: {project_root}")
            logger.error(f"Files in project root: {os.listdir(project_root)}")
            sys.exit(1)

        logger.info(f"Using alembic.ini at: {os.path.abspath(alembic_ini_path)}")
        logger.info(f"Using alembic directory at: {os.path.abspath(alembic_dir_path)}")

        # Create Alembic configuration
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
        alembic_cfg.set_main_option("script_location", alembic_dir_path)

        # Run migrations
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed with error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        print(f"MIGRATION ERROR: {str(e)}")  # Force print to console
        print(traceback.format_exc())  # Force print traceback
        sys.exit(1)

@app.get("/")
def index():
    return 'Hello'


if __name__ == '__main__':
    # Run database migrations before starting the application
    run_migrations()
    logger.info("Starting FastAPI application...")
    logger.info(settings.HOST)
    logger.info(settings.PORT)
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=False)
