from fastapi import APIRouter

from app.notifications.schemas import NotificationCreate
from app.notifications.repository import NotificationRepository
from app.notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])

repository = NotificationRepository()
service = NotificationService(repository)


@router.get("/")
def list_notifications():
    return service.list_notifications()


@router.post("/", status_code=201)
def create_notification(payload: NotificationCreate):
    return service.create_notification(payload)