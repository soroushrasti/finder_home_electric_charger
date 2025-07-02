from fastapi import Depends
from requests import Session
from src.apis.v1.functionalities.activity.service import ActivityService
from src.config.database import create_session
from src.core.db_repository.activity import ActivityRepository, ActivityRepositoryAbstract


class ActivityServiceAbstract:
    pass

class ActivityServiceFactory:
    def __init__(
            self,
            repo: ActivityRepositoryAbstract
            ):
        self.repo = repo

    def get_service(self) -> ActivityService:
        return ActivityService(self.repo)

def get_activity_service(
        db: Session = Depends(create_session)
        ):
    repo = ActivityRepository(db_session=db)
    factory = ActivityServiceFactory(repo=repo)
    return factory.get_service()
