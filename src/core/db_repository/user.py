from typing import Any

from src.core.models import User
from sqlalchemy.orm import Session


class UserRepositoryAbstract:
    def get_user_by_id(self, user_id):
        pass

    def create_user(self, user_data):
        pass

    def login_user(self, username, password):
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

    def login_user(self, username, password):
        user = self.db.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            return user
        return None