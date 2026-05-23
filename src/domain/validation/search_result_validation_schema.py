from __future__ import annotations

from datetime import datetime
from typing import Final

from src.domain.constants.selection import (
    MIN_CANDIDATE_COUNT,
    MIN_RANK,
    MIN_FINAL_SCORE,
)
from src.domain.entities.question import Question
from src.domain.validation.schema_types import (
    ValidationSchema,
)
from src.domain.value_objects.selection_breakdown import (
    SelectionBreakdown,
)


SELECTION_RESULT_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "question": {
        "type": Question,
        "nullable": False,
    },
    "final_score": {
        "type": (int, float),
        "finite": True,
        "reject_bool": True,
        "min_value": MIN_FINAL_SCORE,
        "nullable": False,
    },
    "breakdown": {
        "type": SelectionBreakdown,
        "nullable": False,
    },
    "selected_at": {
        "type": datetime,
        "timezone_aware": True,
        "nullable": False,
    },
    "rank": {
        "type": int,
        "reject_bool": True,
        "min_value": MIN_RANK,
        "nullable": True,
    },
    "candidate_count": {
        "type": int,
        "reject_bool": True,
        "min_value": MIN_CANDIDATE_COUNT,
        "nullable": True,
    },
}