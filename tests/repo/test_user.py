import unittest
from unittest.mock import Mock, patch
import pytest
from typing import Optional, List, Dict, Any

from src.apis.v1.schemas.user import UserType, UpdateUserRequest
from src.core.db_repository.user import UserRepository
from src.core.models import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        # Mock the database session
        self.db_session = Mock()
        self.user_repo = UserRepository(self.db_session)

        # Sample user data for testing
        self.sample_user_data = {
            "user_id": "user123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "username": "john.doe@example.com",  # Same as email by default
            "password": "hashed_password",
            "address_of_home": "123 Main St",
            "city_of_home": "New York",
            "postcode_of_home": "10001",
            "user_type": UserType.HOMEOWNER,
            "mobile_number": "1234567890"
        }

        # Create a sample user object
        self.sample_user = User(**self.sample_user_data)

    def test_create_user(self):
        # Setup
        self.db_session.add.return_value = None
        self.db_session.commit.return_value = None
        self.db_session.refresh.return_value = None

        # Execute
        result = self.user_repo.create_user(self.sample_user_data)

        # Assert
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.db_session.refresh.assert_called_once()
        self.assertEqual(result.email, self.sample_user_data["email"])
        self.assertEqual(result.username, self.sample_user_data["email"])  # Username defaults to email

    def test_get_user_by_id(self):
        # Setup
        user_id = "user123"
        self.db_session.query.return_value.filter.return_value.first.return_value = self.sample_user

        # Execute
        result = self.user_repo.get_user_by_id(user_id)

        # Assert
        self.assertEqual(result, self.sample_user)
        self.db_session.query.assert_called_once()

    def test_get_user_by_id_not_found(self):
        # Setup
        user_id = "nonexistent_user"
        self.db_session.query.return_value.filter.return_value.first.return_value = None

        # Execute
        result = self.user_repo.get_user_by_id(user_id)

        # Assert
        self.assertIsNone(result)

    def test_get_user_by_email(self):
        # Setup
        email = "john.doe@example.com"
        self.db_session.query.return_value.filter.return_value.first.return_value = self.sample_user

        # Execute
        result = self.user_repo.get_user_by_email(email)

        # Assert
        self.assertEqual(result, self.sample_user)

    def test_get_user_by_username(self):
        # Setup
        email = "john.doe@example.com"
        self.db_session.query.return_value.filter.return_value.first.return_value = self.sample_user

        # Execute
        result = self.user_repo.get_user_by_email(email)

        # Assert
        self.assertEqual(result, self.sample_user)

    def test_update_user(self):
        # Setup
        user_id = "123"
        update_data = {"first_name": "Jane", "last_name": "Smith"}
        update_data = UpdateUserRequest(**update_data)
        self.db_session.query.return_value.filter.return_value.first.return_value = self.sample_user
        self.db_session.commit.return_value = None

        # Execute
        result = self.user_repo.update_user(user_id, update_data)

        # Assert
        self.assertEqual(result.first_name, "Jane")
        self.assertEqual(result.last_name, "Smith")
        self.db_session.commit.assert_called_once()
