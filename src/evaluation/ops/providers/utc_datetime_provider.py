from __future__ import annotations

from datetime import datetime
from datetime import timezone


class UTCDateTimeProvider:
    """
    UTC datetime provider.
    """

    @staticmethod
    def now() -> datetime:
        return datetime.now(
            tz=timezone.utc,
        )