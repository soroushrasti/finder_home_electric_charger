from fastapi import Depends
from sqlalchemy.orm import Session, create_session

from src.apis.v1.functionalities.user.service import UserService
from src.core.services.internal.db_repository.user import UserRepository, UserRepositoryAbstract


class UserServiceAbstract:
    pass





class UserServiceFactory:
    def __init__(
            self, 
            repo: UserRepositoryAbstract
            ):
        self.repo = repo

    def get_service(self) -> UserService:
        return UserService(self.repo)

def get_user_service(
        db: Session = Depends(create_session)
        ):
    repo = UserRepository(db=db)
    factory = UserServiceFactory(repo=repo)
    return factory.get_service()
