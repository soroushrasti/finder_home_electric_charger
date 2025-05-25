from fastapi import Depends
from sqlalchemy.orm import Session, create_session

from src.apis.v1.functionalities.charging_location.service import ChargingLocService
from src.core.db_repository.charging_location import ChargingLocRepositoryAbstract, ChargingLocRepository


class ChargingLocServiceAbstract:
    pass


class ChargingLocServiceFactory:
    def __init__(
            self,
            repo: ChargingLocRepositoryAbstract
            ):
        self.repo = repo

    def get_service(self) -> ChargingLocService:
        return ChargingLocService(self.repo)

def get_charging_loc_service(
        db: Session = Depends(create_session)
        ):
    repo = ChargingLocRepository(db_session=db)
    factory = ChargingLocServiceFactory(repo=repo)
    return factory.get_service()
