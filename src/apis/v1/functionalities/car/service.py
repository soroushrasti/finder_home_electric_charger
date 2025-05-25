from src.apis.v1.schemas.car import FindCarRequest
from src.core.db_repository.car import CarRepositoryAbstract, CarRepository


class CarService:
    def __init__(self, car_repo: CarRepository):
        self.car_repo = car_repo

    def get_cars(self, user_id: int):
        return self.car_repo.get_car_by_id(user_id)

    # Add to src/apis/v1/functionalities/user/service.py
    def create_car(self, car_data: dict):
        return self.car_repo.create_car(car_data)

    def find_car(self, find_car_data: FindCarRequest):
        return self.car_repo.find_car(find_car_data)
