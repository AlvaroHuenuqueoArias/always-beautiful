from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock


@dataclass
class ObservabilityState:
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    requests_total: int = 0
    http_errors_total: int = 0
    unhandled_errors_total: int = 0
    _lock: Lock = field(default_factory=Lock, repr=False)

    def increment_requests(self) -> None:
        with self._lock:
            self.requests_total += 1

    def increment_http_errors(self) -> None:
        with self._lock:
            self.http_errors_total += 1

    def increment_unhandled_errors(self) -> None:
        with self._lock:
            self.unhandled_errors_total += 1

    def uptime_seconds(self) -> int:
        return int(
            (datetime.now(timezone.utc) - self.started_at).total_seconds()
        )

    def as_metrics(self) -> dict[str, int | str]:
        return {
            "started_at": self.started_at.isoformat(),
            "uptime_seconds": self.uptime_seconds(),
            "requests_total": self.requests_total,
            "http_errors_total": self.http_errors_total,
            "unhandled_errors_total": self.unhandled_errors_total,
        }


observability_state = ObservabilityState()