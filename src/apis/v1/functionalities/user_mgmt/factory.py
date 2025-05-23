from fastapi import Depends
from sqlalchemy.orm import Session, create_session

from src.apis.v1.functionalities.user_mgmt.service import UserServiceAbstract, UserService
from src.core.services.internal.db_repository.user import UserRepositoryAbstract, UserRepository


class UserServiceFactory:
    def __init__(
            self, 
            repo: UserRepositoryAbstract
            ):
        self.repo = repo

    def get_service(self) -> UserServiceAbstract:
        return UserService(self.repo)

def get_user_service(
        db: Session = Depends(create_session)
        ):
    repo = UserRepository(db_session=db)
    factory = UserServiceFactory(repo=repo)
    return factory.get_service()
