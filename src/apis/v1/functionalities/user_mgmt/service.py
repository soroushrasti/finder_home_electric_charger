import logging, traceback
from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Union, Dict
from fastapi import HTTPException
import marshmallow
from marshmallow import ValidationError

from src.core.services.internal.db_repository.user import UserRepositoryAbstract


class UserServiceAbstract(ABC):
    @abstractmethod
    async def get_user(
        self, 
        email_id: str
    ):
        pass

class UserService(UserServiceAbstract):
    def __init__(
            self, 
            repo: UserRepositoryAbstract
    ) -> None:
        self.repo = repo


