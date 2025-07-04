from src.core.db_repository.user import UserRepositoryAbstract, UserRepository
import bcrypt

from src.core.models import User


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id)

    # Add to src/apis/v1/functionalities/user/service.py
    def create_user(self, user_data: dict):
        user_data['password'] = hash_password(user_data['password'])
        return self.user_repo.create_user(user_data)

    def login_user(self, email, password):
        user: User = self.user_repo.get_user_by_email(email, password)
        if user and check_password(password, user.password):
            return user
        return None

    def validate_user(self,email_verification_code:str,  user_id: int):
        return self.user_repo.validate_user(email_verification_code, user_id)