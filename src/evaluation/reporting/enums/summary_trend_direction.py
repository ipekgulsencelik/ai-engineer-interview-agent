from __future__ import annotations

from enum import StrEnum


class SummaryTrendDirection(
    StrEnum,
):
    """
    Executive summary trend direction.
    """

    IMPROVING = "improving"

    STABLE = "stable"

    DECLINING = "declining"

    VOLATILE = "volatile"

    UNKNOWN = "unknown"