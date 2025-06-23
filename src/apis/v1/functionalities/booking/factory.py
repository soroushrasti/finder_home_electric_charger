from fastapi import Depends
from sqlalchemy.orm import Session
from src.apis.v1.functionalities.booking.service import BookingService
from src.config.database import create_session
from src.apis.v1.functionalities.booking.service import BookingService
from src.core.db_repository.booking import BookingRepositoryAbstract, BookingRepository

class BookingServiceAbstract:
    pass


class BookingServiceFactory:
    def __init__(
            self,
            repo: BookingRepository
            ):
        self.repo = repo

    def get_service(self) -> BookingService:
        return BookingService(self.repo)

def get_booking_service(
        db: Session = Depends(create_session)
        ):
    repo = BookingRepository(db_session=db)
    factory = BookingServiceFactory(repo=repo)
    return factory.get_service()
