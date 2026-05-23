from __future__ import annotations

from typing import Final

from src.domain.constants.evaluation import (
    DEFAULT_RUBRIC_VERSION,
    MAX_CONFIDENCE_SCORE,
    MIN_CONFIDENCE_SCORE,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


NUMBER_TYPES = (int, float)


CONFIDENCE_RULE: Final[
    ValidationRule
] = {
    "type": NUMBER_TYPES,
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_CONFIDENCE_SCORE,
    "max_value": MAX_CONFIDENCE_SCORE,
}


LATENCY_RULE: Final[
    ValidationRule
] = {
    "type": NUMBER_TYPES,
    "nullable": True,
    "reject_bool": True,
    "finite": True,
    "min_value": 0.0,
}


RUBRIC_VERSION_RULE: Final[
    ValidationRule
] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
    "default": DEFAULT_RUBRIC_VERSION,
}


MISSING_KEYWORDS_RULE: Final[
    ValidationRule
] = {
    "type": tuple,
    "nullable": False,
    "item_type": str,
    "non_empty_items": True,
}


FOLLOW_UP_QUESTION_RULE: Final[
    ValidationRule
] = {
    "type": str,
    "nullable": True,
    "non_empty": True,
}


EVALUATION_METADATA_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "confidence": CONFIDENCE_RULE,
    "latency_seconds": LATENCY_RULE,
    "rubric_version": RUBRIC_VERSION_RULE,
    "missing_keywords": MISSING_KEYWORDS_RULE,
    "follow_up_question": FOLLOW_UP_QUESTION_RULE,
}