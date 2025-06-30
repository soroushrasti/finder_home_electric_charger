from requests import Session
from fastapi import Depends
from src.config.database import create_session
from src.apis.v1.functionalities.pricing.service import PricingService
from src.core.db_repository.pricing import PricingRepositoryAbstract, PricingRepository

class PricingServiceAbstract:
    pass

class PricingServiceFactory:
    def __init__(
            self,
            repo: PricingRepositoryAbstract
            ):
        self.repo = repo

    def get_service(self) -> PricingService:
        return PricingService(self.repo)

def get_pricing_service(
        db: Session = Depends(create_session)
        ):
        repo = PricingRepository(db_session=db)
        factory = PricingServiceFactory(repo=repo)
        return factory.get_service()
