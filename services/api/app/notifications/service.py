from uuid import uuid4

from app.notifications.schemas import (
    NotificationCreate,
    NotificationResponse
)
from app.notifications.repository import NotificationRepository


class NotificationService:

    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def create_notification(self, payload: NotificationCreate):

        notification = NotificationResponse(
            id=uuid4(),
            event=payload.event,
            channel=payload.channel,
            recipient=payload.recipient,
            payload=payload.payload,
            status="PENDING"
        )

        return self.repository.save(notification)

    def list_notifications(self):
        return self.repository.list_all()