from fastapi import Depends
from sqlalchemy.orm import Session
from src.config.database import create_session
from src.core.db_repository.public_charger import PublicChargerRepository
from src.apis.v1.functionalities.public_charger.service import PublicChargerService


class PublicChargerServiceFactory:
    def __init__(self, repo: PublicChargerRepository):
        self.repo = repo

    def get_service(self) -> PublicChargerService:
        return PublicChargerService(self.repo)


def get_public_charger_service(db: Session = Depends(create_session)) -> PublicChargerService:
    repo = PublicChargerRepository(db_session=db)
    factory = PublicChargerServiceFactory(repo=repo)
    return factory.get_service()

