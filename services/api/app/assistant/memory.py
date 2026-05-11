from collections import defaultdict

from app.assistant.state import AssistantTurn


class AssistantMemory:
    def __init__(self) -> None:
        self._sessions: dict[str, list[AssistantTurn]] = defaultdict(list)

    def append_turn(self, session_id: str, role: str, content: str) -> None:
        self._sessions[session_id].append(
            AssistantTurn(role=role, content=content)
        )

    def get_session(self, session_id: str) -> list[AssistantTurn]:
        return list(self._sessions.get(session_id, []))

    def reset(self) -> None:
        self._sessions.clear()

