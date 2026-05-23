from __future__ import annotations

from typing import Final

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.constants.interview_state import (
    MAX_TARGET_DIFFICULTY,
    MIN_TARGET_DIFFICULTY,
)
from src.domain.enums.level import Level
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


STRING_TUPLE_RULE: Final[
    ValidationRule
] = {
    "type": tuple,
    "item_type": str,
    "nullable": False,
}


FLOAT_TUPLE_RULE: Final[
    ValidationRule
] = {
    "type": tuple,
    "item_type": (int, float),
    "reject_bool_items": True,
    "min_value": MIN_EVALUATION_SCORE,
    "max_value": MAX_EVALUATION_SCORE,
    "nullable": False,
}


INTERVIEW_STATE_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "current_level": {
        "type": Level,
        "nullable": False,
    },
    "asked_question_ids": STRING_TUPLE_RULE,
    "recent_scores": FLOAT_TUPLE_RULE,
    "weak_categories": STRING_TUPLE_RULE,
    "target_difficulty": {
        "type": int,
        "reject_bool": True,
        "min_value": MIN_TARGET_DIFFICULTY,
        "max_value": MAX_TARGET_DIFFICULTY,
        "nullable": False,
    },
}