from __future__ import annotations

from datetime import datetime
from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_rules import ValidationRule
from src.domain.validation.schema_types import SchemaDefinition

DATETIME_OBJECT_RULE: Final[ValidationRule] = ValidationRule(expected_type=datetime)

EVALUATION_RUN_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "run_id": NON_EMPTY_STRING_RULE,
    "started_at": DATETIME_OBJECT_RULE,
    "completed_at": DATETIME_OBJECT_RULE,
    "duration_seconds": NON_NEGATIVE_NUMBER_RULE,
    "success": BOOLEAN_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}
