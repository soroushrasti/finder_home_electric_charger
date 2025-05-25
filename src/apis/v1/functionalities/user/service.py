from src.core.db_repository.user import UserRepositoryAbstract, UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id)

    # Add to src/apis/v1/functionalities/user/service.py
    def create_user(self, user_data: dict):
        return self.user_repo.create_user(user_data)

    def login_user(self, username, password):
        return self.user_repo.login_user(username, password)