from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from src.config.base import BaseConfig

# Create SQLite engine - adjust the path as needed
SQLALCHEMY_DATABASE_URL = BaseConfig().DATABASE_URL
print(f"{SQLALCHEMY_DATABASE_URL[0:10]}*****")  # Debugging line to check the URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_session() -> Generator[Session, None, None]:
    """Creates a SQLite database session and ensures it's closed after use"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()