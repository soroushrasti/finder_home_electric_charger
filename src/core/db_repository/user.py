from typing import Any

from sqlalchemy.testing.suite.test_reflection import users

from src.core.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from cmath import e


class UserRepositoryAbstract:
    def get_user_by_id(self, user_id):
        pass

    def create_user(self, user_data):
        pass

    def get_user_by_email(self, username, password):
        pass


class UserRepository(UserRepositoryAbstract):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> type[User] | None:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def create_user(self, user_data: dict) -> User:
        new_user = User(**user_data)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user_by_email(self, email, password):
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def validate_user(self, email_verification_code: str, user_id: int):
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if user.email_verification_code == email_verification_code:
              user.is_validated = True
              self.db.commit()
              self.db.refresh(user)
              return user
        else:
               raise HTTPException(
                   status_code=status.HTTP_404_BAD_REQUEST,
                   detail=f"Error validate user: {str(e)}"
                )

