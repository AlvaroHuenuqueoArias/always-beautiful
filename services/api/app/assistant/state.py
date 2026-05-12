from enum import Enum
from typing import Any, TypedDict

from pydantic import BaseModel, Field


class AssistantIntent(str, Enum):
    BOOKING = "booking"
    BOOKING_CONVERSION = "booking_conversion"
    PRODUCT_RECOMMENDATION = "product_recommendation"
    GENERAL = "general"


class AssistantFlowStep(str, Enum):
    COMPLETED = "completed"
    SERVICE_SELECTION = "service_selection"
    PROFESSIONAL_SELECTION = "professional_selection"
    DATE_SELECTION = "date_selection"
    TIME_SELECTION = "time_selection"
    AVAILABILITY_CHECK = "availability_check"
    DEPOSIT_CONFIRMATION = "deposit_confirmation"
    CHECKOUT_REDIRECT = "checkout_redirect"
    PRODUCT_SELECTION = "product_selection"


DEFAULT_ASSISTANT_FLOW_STEP = AssistantFlowStep.COMPLETED.value


class AssistantChannel(str, Enum):
    WEB = "web"
    WHATSAPP = "whatsapp"
    ADMIN = "admin"


class AssistantState(TypedDict, total=False):
    session_id: str
    message: str
    channel: str
    intent: str
    flow_step: str
    response_message: str
    requires_deposit: bool
    deposit_percentage: int
    next_actions: list[str]
    metadata: dict[str, Any]


class AssistantTurn(BaseModel):
    role: str = Field(..., min_length=1, max_length=40)
    content: str = Field(..., min_length=1, max_length=4000)
