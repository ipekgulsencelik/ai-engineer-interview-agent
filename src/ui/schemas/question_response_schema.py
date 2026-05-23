from __future__ import annotations

from typing import Final

from src.domain.validation.schema_types import (
    ValidationRule,
)


NUMBER_TYPES: Final[tuple[type[int], type[float]]] = (
    int,
    float,
)

MIN_QUESTION_DIFFICULTY: Final[int] = 1

MIN_RETRIEVAL_SCORE: Final[float] = 0.0


QUESTION_RESPONSE_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}


QUESTION_RESPONSE_DIFFICULTY_RULE: Final[ValidationRule] = {
    "type": int,
    "nullable": False,
    "reject_bool": True,
    "min_value": MIN_QUESTION_DIFFICULTY,
}


QUESTION_RESPONSE_SCORE_RULE: Final[ValidationRule] = {
    "type": NUMBER_TYPES,
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_RETRIEVAL_SCORE,
}