from __future__ import annotations

from typing import Final

from src.domain.constants.coverage import (
    MIN_COVERAGE_COUNT,
    MIN_TOTAL_QUESTIONS,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


COUNT_MAPPING_RULE: Final[ValidationRule] = {
    "type": dict,
    "key_type": str,
    "value_type": int,
    "reject_bool_values": True,
    "min_value": MIN_COVERAGE_COUNT,
    "nullable": False,
}


TOTAL_QUESTIONS_RULE: Final[ValidationRule] = {
    "type": int,
    "reject_bool": True,
    "min_value": MIN_TOTAL_QUESTIONS,
    "nullable": False,
}


INTERVIEW_COVERAGE_VALIDATION_SCHEMA: Final[ValidationSchema] = {
    "category_counts": COUNT_MAPPING_RULE,
    "level_counts": COUNT_MAPPING_RULE,
    "question_type_counts": COUNT_MAPPING_RULE,
    "total_questions": TOTAL_QUESTIONS_RULE,
}