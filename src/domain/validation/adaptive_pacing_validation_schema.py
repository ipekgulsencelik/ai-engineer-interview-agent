from __future__ import annotations

from typing import Final

from src.domain.constants.adaptive_pacing import (
    MAX_TARGET_DIFFICULTY,
    MIN_DIFFICULTY_MULTIPLIER,
    MIN_TARGET_DIFFICULTY,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


TARGET_DIFFICULTY_RULE: Final[
    ValidationRule
] = {
    "type": int,
    "reject_bool": True,
    "min_value": MIN_TARGET_DIFFICULTY,
    "max_value": MAX_TARGET_DIFFICULTY,
    "nullable": False,
}


MULTIPLIER_RULE: Final[
    ValidationRule
] = {
    "type": (int, float),
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_DIFFICULTY_MULTIPLIER,
    "nullable": False,
}


BOOLEAN_FLAG_RULE: Final[
    ValidationRule
] = {
    "type": bool,
    "nullable": False,
}


ADAPTIVE_PACING_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "target_difficulty": (
        TARGET_DIFFICULTY_RULE
    ),
    "difficulty_multiplier": (
        MULTIPLIER_RULE
    ),
    "should_reduce_difficulty": (
        BOOLEAN_FLAG_RULE
    ),
    "should_increase_difficulty": (
        BOOLEAN_FLAG_RULE
    ),
}