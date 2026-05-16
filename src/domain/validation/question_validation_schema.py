from __future__ import annotations

from typing import Any, Final

from src.domain.constants.question import (
    MAX_DIFFICULTY,
    MAX_MARKET_WEIGHT,
    MIN_DIFFICULTY,
    MIN_MARKET_WEIGHT,
)
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType

NUMBER_TYPES: Final[tuple[type[int], type[float]]] = (
    int,
    float,
)

QUESTION_VALIDATION_SCHEMA: Final[dict[str, dict[str, Any]]] = {
    "id": {
        "type": str,
        "non_empty": True,
    },
    "text": {
        "type": str,
        "non_empty": True,
    },
    "category": {
        "type": QuestionCategory,
    },
    "level": {
        "type": Level,
    },
    "difficulty": {
        "type": int,
        "min_value": MIN_DIFFICULTY,
        "max_value": MAX_DIFFICULTY,
    },
    "question_type": {
        "type": QuestionType,
    },
    "expected_points": {
        "type": list,
        "item_type": str,
    },
    "keywords": {
        "type": list,
        "item_type": str,
    },
    "followup": {
        "type": str,
        "non_empty": True,
        "nullable": True,
    },
    "ideal_answer_hint": {
        "type": str,
        "non_empty": True,
        "nullable": True,
    },
    "market_weight": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_MARKET_WEIGHT,
        "max_value": MAX_MARKET_WEIGHT,
    },
    "followup_allowed": {
        "type": bool,
    },
}