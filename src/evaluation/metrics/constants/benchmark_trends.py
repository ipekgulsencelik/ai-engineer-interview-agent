from __future__ import annotations

from typing import Final


IMPROVING_TREND_DIRECTION: Final[str] = "improving"
STABLE_TREND_DIRECTION: Final[str] = "stable"
DEGRADING_TREND_DIRECTION: Final[str] = "degrading"


VALID_TREND_DIRECTIONS: Final[frozenset[str]] = frozenset(
    {
        IMPROVING_TREND_DIRECTION,
        STABLE_TREND_DIRECTION,
        DEGRADING_TREND_DIRECTION,
    }
)