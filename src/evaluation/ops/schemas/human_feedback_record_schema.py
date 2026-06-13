from __future__ import annotations

from typing import Final
from datetime import datetime

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_BOOLEAN_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)
from src.domain.validation.schema_rules import (
    ValidationRule,
)


DATETIME_OBJECT_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=datetime,
)


HUMAN_FEEDBACK_RECORD_SCHEMA: Final[SchemaDefinition] = {
    "feedback_id": NON_EMPTY_STRING_RULE,
    "evaluator_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_OBJECT_RULE,
    "sample_id": OPTIONAL_STRING_RULE,
    "reviewer_id": OPTIONAL_STRING_RULE,
    "rating": OPTIONAL_RATIO_RULE,
    "score": OPTIONAL_RATIO_RULE,
    "is_accepted": OPTIONAL_BOOLEAN_RULE,
    "comment": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}
