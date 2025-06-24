from src.apis.v1.schemas.notification import FindNotificationRequest
from src.apis.v1.schemas.notification import FindNotificationRequest
from src.core.db_repository.notification import NotificationRepository
from src.core.db_repository.notification import NotificationRepositoryAbstract, NotificationRepository


class NotificationService:
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def get_notifications(self, booking_id: int):
        return self.notification_repo.get_notification_by_id(booking_id)

    # Add to src/apis/v1/functionalities/user/service.py
    def create_notification(self, notification_data: dict):
        return self.notification_repo.create_notification(notification_data)

    def find_notification(self, find_notification_data: FindNotificationRequest):
        return self.notification_repo.find_notification(find_notification_data)
