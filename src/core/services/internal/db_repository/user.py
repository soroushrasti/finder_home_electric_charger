from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Optional, Union
from sqlalchemy.sql import exists
from sqlalchemy import func

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

class UserRepository(UserRepositoryAbstract):
    def __init__(self, db_session: Session) -> None:
        super().__init__()
        self.db_session = db_session

