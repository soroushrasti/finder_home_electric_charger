from cmath import e
from fastapi import HTTPException
from src.apis.v1.schemas.car import FindCarRequest
from src.core.models import Car
from starlette import status


class CarRepositoryAbstract:
    pass


class CarRepository(CarRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_car_by_id(self, user_id: int):
        return self.db_session.query(Car).filter(Car.user_id == user_id).all()

    def create_car(self, car_data: dict):
        new_car = Car(**car_data)
        self.db_session.add(new_car)
        self.db_session.commit()
        return new_car

    def update_car(self, car_id: int, car_data: dict):
        # Logic to update an existing car in the database
        new_car = Car(**car_data)
        query = self.db_session.query(Car).filter(Car.car_id == car_id).first()
        if query:
            query.user_id= new_car.user_id
            query.model = new_car.model
            query.color = new_car.color
            query.year = new_car.year
            query.license_plate = new_car.license_plate
            self.db_session.add(query)
            self.db_session.commit()
            return query
        else:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error finding booking: {str(e)}"
            )

    def delete_car(self, car_id: int):
        # Logic to delete a car from the database
        pass

    def find_car(self, find_car_data: FindCarRequest):
        query = self.db_session.query(Car)

        if find_car_data.user_id:
            query = query.filter(Car.user_id == find_car_data.user_id)
        if find_car_data.model:
            query = query.filter(Car.model == find_car_data.model)
        if find_car_data.year:
            query = query.filter(Car.year == find_car_data.year)
        if find_car_data.color:
            query = query.filter(Car.color == find_car_data.color)
        if find_car_data.license_plate:
            query = query.filter(Car.license_plate == find_car_data.license_plate)

        return query.all()
