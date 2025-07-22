import unittest
from unittest.mock import Mock

from src.apis.v1.schemas.car import UpdateCarRequest, FindCarRequest
from src.core.db_repository.car import CarRepository
from src.core.models import Car


class TestCarRepository(unittest.TestCase):
    def setUp(self):
        # Mock the database session
        self.db_session = Mock()
        self.car_repo = CarRepository(self.db_session)

        # Sample car data for testing
        self.sample_car_data = {
            "car_id": "1",
            "user_id": "2",
            "model": "benz",
            "color": "red",
            "year": "2024",
            "license_plate": "124p13",
        }
        # Create a sample car object
        self.sample_car = Car(**self.sample_car_data)

    def test_create_car(self):
        # Setup
        self.db_session.add.return_value = None
        self.db_session.commit.return_value = None
        self.db_session.refresh.return_value = None

        # Execute
        result = self.car_repo.create_car(self.sample_car_data)

        # Assert
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.assertEqual(result.year, self.sample_car_data["year"])
        self.assertEqual(result.model, self.sample_car_data["model"])

    def test_update_car(self):
        # Setup
        car_id = "1"
        update_data = {"model": "toyota", "color": "green"}
        update_data = UpdateCarRequest(**update_data)
        self.db_session.query.return_value.filter.return_value.first.return_value = self.sample_car
        self.db_session.commit.return_value = None

        # Execute
        result = self.car_repo.update_car(car_id, update_data)

        # Assert
        self.assertEqual(result.model, "toyota")
        self.assertEqual(result.color, "green")
        self.db_session.commit.assert_called_once()

    def test_get_car_by_id(self):
            # Setup
            user_id = "2"
            self.db_session.query.return_value.filter.return_value.all.return_value = [self.sample_car]

            # Execute
            result = self.car_repo.get_cars_by_id(user_id)

            # Assert
            self.assertEqual(result,[ self.sample_car])
            self.db_session.query.assert_called_once()

    def test_get_car_by_id_not_found(self):
        # Setup
        user_id = "nonexistent_user"
        self.db_session.query.return_value.filter.return_value.all.return_value = []

        # Execute
        result = self.car_repo.get_cars_by_id(user_id)

        # Assert
        self.assertEqual(result, [])

    # def test_find_car(self):
    #     self.db_session.query.return_value.filter.return_value.first.return_value = [self.sample_car]
    #
    #     # Execute
    #     # find_car_sample = FindCarRequest(**self.sample_car_data)
    #     result = self.car_repo.find_car(self.sample_car)
    #
    #     # Assert
    #     self.assertEqual(result, [self.sample_car])
    #     self.db_session.query.assert_called_once()

