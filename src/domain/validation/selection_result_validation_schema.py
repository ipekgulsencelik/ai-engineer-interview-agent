from __future__ import annotations

from datetime import datetime
from typing import Any

from src.domain.constants.selection import (
    MIN_CANDIDATE_COUNT,
    MIN_RANK,
    MIN_SELECTION_SCORE,
)
from src.domain.entities.question import Question
from src.domain.results.selection_breakdown import SelectionBreakdown


NUMBER_TYPES = (int, float)


SELECTION_RESULT_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "question": {
        "type": Question,
    },
    "final_score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_SELECTION_SCORE,
    },
    "breakdown": {
        "type": SelectionBreakdown,
    },
    "selected_at": {
        "type": datetime,
        "timezone_aware": True,
    },
    "rank": {
        "type": int,
        "nullable": True,
        "min_value": MIN_RANK,
    },
    "candidate_count": {
        "type": int,
        "nullable": True,
        "min_value": MIN_CANDIDATE_COUNT,
    },
}