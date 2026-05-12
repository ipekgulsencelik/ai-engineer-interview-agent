from __future__ import annotations

from datetime import datetime
from typing import TypedDict

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.enums.level import Level
from src.domain.results.evaluation_result import EvaluationResult


class FieldRule(TypedDict, total=False):
    type: type | tuple[type, ...]
    item_type: type | tuple[type, ...]
    non_empty: bool
    finite: bool
    min_value: float
    max_value: float
    timezone_aware: bool


INTERVIEW_SESSION_VALIDATION_SCHEMA: dict[str, FieldRule] = {
    "session_id": {
        "type": str,
        "non_empty": True,
    },
    "current_level": {
        "type": Level,
    },
    "asked_question_ids": {
        "type": tuple,
        "item_type": str,
    },
    "completed_results": {
        "type": tuple,
        "item_type": EvaluationResult,
    },
    "recent_scores": {
        "type": tuple,
        "item_type": (int, float),
        "finite": True,
        "min_value": MIN_EVALUATION_SCORE,
        "max_value": MAX_EVALUATION_SCORE,
    },
    "started_at": {
        "type": datetime,
        "timezone_aware": True,
    },
}