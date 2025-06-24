from fastapi import Depends
from sqlalchemy.orm import Session
from src.apis.v1.functionalities.notification.service import NotificationService
from src.config.database import create_session
from src.apis.v1.functionalities.notification.service import NotificationService
from src.core.db_repository.notification import NotificationRepositoryAbstract, NotificationRepository

class NotificationServiceAbstract:
    pass


class NotificationServiceFactory:
    def __init__(
            self,
            repo: NotificationRepository
            ):
        self.repo = repo

    def get_service(self) -> NotificationService:
        return NotificationService(self.repo)

def get_notification_service(
        db: Session = Depends(create_session)
        ):
    repo = NotificationRepository(db_session=db)
    factory = NotificationServiceFactory(repo=repo)
    return factory.get_service()
