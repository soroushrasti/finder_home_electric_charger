from src.apis.v1.schemas.notification import FindNotificationRequest
from src.core.models import Notification


class NotificationRepositoryAbstract:
    pass


class NotificationRepository(NotificationRepositoryAbstract):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_notification_by_id(self, booking_id: int):
        return self.db_session.query(Notification).filter(Notification.booking_id == booking_id).all()

    def create_notification(self, notification_data: dict):
        new_notification = Notification(**notification_data)
        self.db_session.add(new_notification)
        self.db_session.commit()
        return new_notification

    def update_notification(self, notification_id: int, notification_data: dict):
        # Logic to update an existing car in the database
        pass

    def delete_notification(self, notification_id: int):
        # Logic to delete a car from the database
        pass

    def find_notification(self, find_notification_data: FindNotificationRequest):
        query = self.db_session.query(Notification)

        if find_notification_data.booking_id:
            query = query.filter(Notification.booking_id == find_notification_data.booking_id)
        if find_notification_data.message:
            query = query.filter(Notification.booking_id == find_notification_data.message)
        if find_notification_data.is_read:
            query = query.filter(Notification.booking_id == find_notification_data.is_read)
        if find_notification_data.level:
            query = query.filter(Notification.booking_id == find_notification_data.level)


        return query.all()
