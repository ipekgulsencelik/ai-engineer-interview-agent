from __future__ import annotations

from datetime import datetime, timezone

from src.application.ports.clock import Clock


class SystemClock(Clock):
    """
    UTC system clock implementation.
    """

    def now(self) -> datetime:
        return datetime.now(timezone.utc)