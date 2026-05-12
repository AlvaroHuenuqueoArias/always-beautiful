from pydantic import BaseModel, Field, field_validator

from app.assistant.state import AssistantChannel, AssistantFlowStep, AssistantIntent


class AssistantChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=120)
    message: str = Field(..., min_length=1, max_length=2000)
    channel: AssistantChannel

    @field_validator("session_id", "message")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Value must not be blank")
        return cleaned


class AssistantChatResponse(BaseModel):
    session_id: str
    intent: AssistantIntent
    flow_step: AssistantFlowStep = AssistantFlowStep.COMPLETED
    message: str
    requires_deposit: bool
    deposit_percentage: int
    next_actions: list[str]
