from src.core.services.models import User
from sqlalchemy.orm import Session


class UserRepositoryAbstract:
    def get_user_by_id(self, user_id):
        pass

class UserRepository(UserRepositoryAbstract):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: dict) -> User:
        new_user = User(**user_data)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user