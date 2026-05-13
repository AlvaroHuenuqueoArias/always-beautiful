from app.assistant.graph import AssistantGraphRunner
from app.assistant.memory import AssistantMemory
from app.assistant.schemas import AssistantChatRequest, AssistantChatResponse
from app.assistant.state import (
    DEFAULT_ASSISTANT_FLOW_STEP,
    AssistantFlowStep,
    AssistantIntent,
    AssistantState,
)


class AssistantService:
    def __init__(
        self,
        graph_runner: AssistantGraphRunner | None = None,
        memory: AssistantMemory | None = None,
    ) -> None:
        self.graph_runner = graph_runner or AssistantGraphRunner()
        self.memory = memory or AssistantMemory()

    def chat(self, payload: AssistantChatRequest) -> AssistantChatResponse:
        history = self.memory.get_session(payload.session_id)
        state: AssistantState = {
            "session_id": payload.session_id,
            "message": payload.message,
            "channel": payload.channel.value,
            "metadata": {"history_size": len(history)},
        }

        result = self.graph_runner.run(state)

        response = AssistantChatResponse(
            session_id=payload.session_id,
            intent=AssistantIntent(result["intent"]),
            flow_step=AssistantFlowStep(
                result.get("flow_step", DEFAULT_ASSISTANT_FLOW_STEP)
            ),
            message=result["response_message"],
            requires_deposit=result["requires_deposit"],
            deposit_percentage=result["deposit_percentage"],
            next_actions=result["next_actions"],
            redirect_target=result.get("redirect_target"),
            cart_payload=result.get("cart_payload"),
        )

        self.memory.append_turn(payload.session_id, "user", payload.message)
        self.memory.append_turn(payload.session_id, "assistant", response.message)

        return response
