from fastapi import APIRouter, status

from app.assistant.schemas import AssistantChatRequest, AssistantChatResponse
from app.assistant.service import AssistantService


router = APIRouter(prefix="/assistant", tags=["assistant"])

assistant_service = AssistantService()


@router.get("/health", status_code=status.HTTP_200_OK)
def assistant_health() -> dict[str, str]:
    return {"status": "ok", "module": "assistant"}


@router.post(
    "/chat",
    response_model=AssistantChatResponse,
    status_code=status.HTTP_200_OK,
)
def assistant_chat(payload: AssistantChatRequest) -> AssistantChatResponse:
    return assistant_service.chat(payload)

