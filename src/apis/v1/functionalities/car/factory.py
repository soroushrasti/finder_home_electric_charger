from fastapi import Depends
from sqlalchemy.orm import Session
from src.config.database import create_session

from src.apis.v1.functionalities.car.service import CarService
from src.core.db_repository.car import CarRepositoryAbstract, CarRepository

class CarServiceAbstract:
    pass


class CarServiceFactory:
    def __init__(
            self,
            repo: CarRepositoryAbstract
            ):
        self.repo = repo

    def get_service(self) -> CarService:
        return CarService(self.repo)

def get_car_service(
        db: Session = Depends(create_session)
        ):
    repo = CarRepository(db=db)
    factory = CarServiceFactory(repo=repo)
    return factory.get_service()
