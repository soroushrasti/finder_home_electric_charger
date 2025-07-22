import unittest
from unittest.mock import Mock

from src.apis.v1.schemas.booking import UpdateBookingRequest
from src.core.db_repository.booking import BookingRepository
from src.core.models import Booking


class TestBookingRepository(unittest.TestCase):
    def setUp(self):
        # Mock the database session
        self.db_session = Mock()
        self.booking_repo = BookingRepository(self.db_session)

        # Sample booking data for testing
        self.sample_booking_data = {
            "booking_id": "1",
            "car_id": "2",
            "charging_location_id": "4",
            "start_time": "2023-10-01 15:00:00",
            "end_time": "2023-10-01 16:00:00",
            "review_rate": "5",
            "review_message": "4",
            "status": "fail",

        }
        # Create a sample booking object
        self.sample_booking = Booking(**self.sample_booking_data)

    def test_create_booking(self):
            # Setup
            self.db_session.add.return_value = None
            self.db_session.commit.return_value = None

            # Execute
            result = self.booking_repo.create_booking(self.sample_booking_data)

            # Assert
            self.db_session.add.assert_called_once()
            self.db_session.commit.assert_called_once()
            self.assertEqual(result.car_id, self.sample_booking_data["car_id"])
            self.assertEqual(result.review_message, self.sample_booking_data["review_message"])

    def test_update_booking(self):
        # Setup
        booking_id = "1"
        update_data = {"charging_location_id": "4", "start_time": "2023-10-01 15:00:00"}
        update_data = UpdateBookingRequest(**update_data)
        self.db_session.query.return_value.filter.return_value.first.return_value = self.sample_booking
        self.db_session.commit.return_value = None

        # Execute
        result = self.booking_repo.update_booking(booking_id, update_data)

        # Assert
        self.assertEqual(str(result.charging_location_id), self.sample_booking_data["charging_location_id"])
        self.assertEqual(str(result.start_time), self.sample_booking_data["start_time"])
        self.db_session.commit.assert_called_once()

    def test_get_booking_by_id(self):
            # Setup
            car_id = "2"
            self.db_session.query.return_value.filter.return_value.all.return_value = [self.sample_booking]

            # Execute
            result = self.booking_repo.get_booking_by_id(car_id)

            # Assert
            self.assertEqual(result, [self.sample_booking])
            self.db_session.query.assert_called_once()

    def test_get_booking_by_id_not_found(self):
        # Setup
        user_id = "nonexistent_user"
        self.db_session.query.return_value.filter.return_value.all.return_value = []

        # Execute
        result = self.booking_repo.get_booking_by_id(user_id)

        # Assert
        self.assertEqual(result, [])

    def test_find_booking(self):
        pass
