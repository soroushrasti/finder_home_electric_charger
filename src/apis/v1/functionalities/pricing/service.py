from src.apis.v1.schemas.pricing import FindPricingRequest
from src.core.db_repository.pricing import PricingRepositoryAbstract, PricingRepository


class PricingService:
    def __init__(self, pricing_repo: PricingRepository):
        self.pricing_repo = pricing_repo

    def create_pricing(self, pricing_data: dict):
        return self.pricing_repo.create_pricing(pricing_data)

    def find_pricing(self, find_pricing_data: FindPricingRequest):
        return self.pricing_repo.find_pricing(find_pricing_data)
