from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Optional, Union
from sqlalchemy.sql import exists
from sqlalchemy import func
from src.core.services.models import User, UserProfile, UserHistory, UserProfileHistory,  Segment
from src.apis.v1.schemas.user import users_schema, user_profile_schema, UserUpdateSchema, UserCreationSchema, users_list_schema

class UserRepositoryAbstract(ABC):
    @abstractmethod
    async def get_user_by_email(
            self,
            user_email: str
    ):
        pass

    @abstractmethod
    async def get_user_by_id(
            self,
            user_id: int
    ):
        pass

    @abstractmethod
    async def get_all_users(
            self
    ):
        pass
    
    @abstractmethod
    async def check_username(
            self,
            username: str
    ) -> bool:
        pass

