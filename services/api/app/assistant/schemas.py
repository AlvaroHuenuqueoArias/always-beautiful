from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.assistant.state import AssistantChannel, AssistantFlowStep, AssistantIntent


class AssistantChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=120)
    message: str = Field(..., min_length=1, max_length=2000)
    channel: AssistantChannel
    context: dict[str, Any] | None = None

    @field_validator("session_id", "message")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Value must not be blank")
        return cleaned


class AssistantBookingDepositCartPayload(BaseModel):
    type: Literal["booking_deposit"] = "booking_deposit"
    status: Literal["pending_deposit"] = "pending_deposit"
    deposit_percentage: int = Field(..., ge=0, le=100)
    remaining_percentage: int = Field(..., ge=0, le=100)
    amount_status: Literal["pending_final_price"] = "pending_final_price"
    service_label: str = Field(..., min_length=1)
    professional_label: str = Field(..., min_length=1)
    selected_service: str = Field(..., min_length=1)
    selected_professional: str = Field(..., min_length=1)
    professional_id: str = Field(..., min_length=1)
    professional_role: str = Field(..., min_length=1)
    requested_day: str | None = None
    requested_time: str | None = None
    confirmation_status: Literal["not_confirmed"] = "not_confirmed"
    payment_status: Literal["deposit_pending"] = "deposit_pending"
    schedule_status: Literal[
        "pending_selection",
        "pending_confirmation",
    ] = "pending_selection"
    items: list[dict[str, Any]] = Field(default_factory=list)
    total_items: int | None = Field(default=None, ge=0)
    cart_count: int | None = Field(default=None, ge=0)


class AssistantQuickReply(BaseModel):
    label: str = Field(..., min_length=1, max_length=80)
    message: str = Field(..., min_length=1, max_length=500)
    action_type: Literal["reply", "navigate", "cart_handoff"]
    target: str | None = None
    payload: dict[str, Any] | None = None


class AssistantChatResponse(BaseModel):
    session_id: str
    intent: AssistantIntent
    flow_step: AssistantFlowStep = AssistantFlowStep.COMPLETED
    message: str
    requires_deposit: bool
    deposit_percentage: int
    next_actions: list[str]
    redirect_target: str | None = None
    cart_payload: AssistantBookingDepositCartPayload | None = None
    context: dict[str, Any] = Field(default_factory=dict)
    quick_replies: list[AssistantQuickReply] = Field(default_factory=list)
