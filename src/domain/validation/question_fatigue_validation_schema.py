from __future__ import annotations

from typing import Final

from src.domain.constants.fatigue import (
    MIN_FATIGUE_COUNT,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


NON_NEGATIVE_COUNT_RULE: Final[
    ValidationRule
] = {
    "type": int,
    "reject_bool": True,
    "min_value": MIN_FATIGUE_COUNT,
    "nullable": False,
}


QUESTION_FATIGUE_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "repeated_category_count": (
        NON_NEGATIVE_COUNT_RULE
    ),
    "repeated_question_type_count": (
        NON_NEGATIVE_COUNT_RULE
    ),
    "recent_high_difficulty_count": (
        NON_NEGATIVE_COUNT_RULE
    ),
}