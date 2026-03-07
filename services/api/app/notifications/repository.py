from typing import Dict, List
from uuid import UUID

from app.notifications.schemas import NotificationResponse


class NotificationRepository:

    def __init__(self):
        self._notifications: Dict[UUID, NotificationResponse] = {}

    def save(self, notification: NotificationResponse):
        self._notifications[notification.id] = notification
        return notification

    def list_all(self) -> List[NotificationResponse]:
        return list(self._notifications.values())