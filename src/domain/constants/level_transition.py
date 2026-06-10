from __future__ import annotations

from typing import Final


MIN_REQUIRED_RECENT_SCORES: Final[int] = 1


RECENT_SCORES_MUST_BE_LIST_ERROR = (
    "recent_scores must be a list."
)

RECENT_SCORES_MUST_CONTAIN_NUMBERS_ERROR = (
    "recent_scores must contain numbers."
)

RECENT_SCORES_MUST_BE_FINITE_ERROR = (
    "Scores must be finite numbers."
)

RECENT_SCORES_RANGE_ERROR = (
    "Scores must be between 0 and 10."
)