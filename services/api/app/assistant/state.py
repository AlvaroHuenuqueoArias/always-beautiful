from enum import Enum
from typing import Any, TypedDict

from pydantic import BaseModel, Field


class AssistantIntent(str, Enum):
    BOOKING = "booking"
    PRODUCT_RECOMMENDATION = "product_recommendation"
    GENERAL = "general"


class AssistantChannel(str, Enum):
    WEB = "web"
    WHATSAPP = "whatsapp"
    ADMIN = "admin"


class AssistantState(TypedDict, total=False):
    session_id: str
    message: str
    channel: str
    intent: str
    response_message: str
    requires_deposit: bool
    deposit_percentage: int
    next_actions: list[str]
    metadata: dict[str, Any]


class AssistantTurn(BaseModel):
    role: str = Field(..., min_length=1, max_length=40)
    content: str = Field(..., min_length=1, max_length=4000)

