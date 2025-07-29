import subprocess
import sys
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Check if DATABASE_URL_SQLALCHEMY is set
    db_url = BaseConfig().DATABASE_URL
    if not db_url:
        logger.error("DATABASE_URL_SQLALCHEMY environment variable is not set")
        logger.info("Set it with: export DATABASE_URL='sqlite:///src/database.db'")
        sys.exit(1)

    try:
        logger.info(f"Running database migrations with URL: {db_url[:20]}...")
        subprocess.run(["poetry", "run", "alembic", "upgrade", "head"], check=True)
        logger.info("Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()