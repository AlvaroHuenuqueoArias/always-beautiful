from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Dict


class NotificationCreate(BaseModel):
    event: str
    channel: str
    recipient: EmailStr
    payload: Dict


class NotificationResponse(BaseModel):
    id: UUID
    event: str
    channel: str
    recipient: EmailStr
    payload: Dict
    status: str