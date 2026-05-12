from __future__ import annotations

from typing import Any

from src.domain.constants.selection import (
    MIN_RANK,
    MIN_SELECTION_SCORE,
)
from src.domain.entities.question import Question
from src.domain.results.selection_breakdown import SelectionBreakdown


NUMBER_TYPES = (int, float)


RANKED_CANDIDATE_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "question": {
        "type": Question,
    },
    "final_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "non_negative": True,
        "min_value": MIN_SELECTION_SCORE,
    },
    "breakdown": {
        "type": SelectionBreakdown,
    },
    "rank": {
        "type": int,
        "non_negative": True,
        "min_value": MIN_RANK,
    },
}