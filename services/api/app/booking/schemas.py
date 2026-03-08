from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class BookingStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class BookingCreate(BaseModel):
    professional_id: str = Field(..., min_length=1, max_length=100)
    service_name: str = Field(..., min_length=1, max_length=150)
    client_name: str = Field(..., min_length=2, max_length=120)
    client_email: EmailStr
    start_at: datetime
    end_at: datetime
    notes: Optional[str] = Field(default=None, max_length=500)


class BookingResponse(BaseModel):
    id: UUID
    professional_id: str
    service_name: str
    client_name: str
    client_email: EmailStr
    start_at: datetime
    end_at: datetime
    status: BookingStatus
    notes: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    status: BookingStatus