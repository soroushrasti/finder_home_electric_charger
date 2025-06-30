from src.apis.v1.schemas.pricing import FindPricingRequest
from src.core.models import Car, ChargingLocation, Pricing


class PricingRepositoryAbstract:
    pass


class PricingRepository(PricingRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def create_pricing(self, pricing_data: dict):
        new_pricing= Pricing(**pricing_data)
        self.db_session.add(new_pricing)
        self.db_session.commit()
        return new_pricing

    def find_pricing(self, find_pricing_data: FindPricingRequest):
        query = (self.db_session.query(Pricing).join(Car).filter(Car.car_id == Car.car_id).
                 join(ChargingLocation).filter(ChargingLocation.charging_location_id ==Pricing.charging_location_id))

        if find_pricing_data.pricing_id:
            query = query.filter(Pricing.pricing_id == find_pricing_data.pricing_id)
        if find_pricing_data.currency:
            query = query.filter(Pricing.currency == find_pricing_data.currency)
        if find_pricing_data.total_value:
            query = query.filter(Pricing.total_value == find_pricing_data.total_value)
        if find_pricing_data.price_per_khw:
            query = query.filter(Pricing.price_per_khw == find_pricing_data.price_per_khw)
        if find_pricing_data.charger_location_owner_user_id:
            query = query.filter(ChargingLocation.user_id == find_pricing_data.charger_location_owner_user_id)
        if find_pricing_data.car_owner_user_id:
            query = query.filter(Car.user_id == find_pricing_data.car_owner_user_id)

        return query.all()
