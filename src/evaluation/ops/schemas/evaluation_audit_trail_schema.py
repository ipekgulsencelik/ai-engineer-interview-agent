from __future__ import annotations

from datetime import datetime
from typing import Final

from src.domain.validation.common_rules import NON_EMPTY_STRING_RULE
from src.domain.validation.schema_rules import ValidationRule
from src.domain.validation.schema_types import SchemaDefinition

DATETIME_OBJECT_RULE: Final[ValidationRule] = ValidationRule(expected_type=datetime)

EVALUATION_AUDIT_TRAIL_SCHEMA: Final[SchemaDefinition] = {
    "trail_id": NON_EMPTY_STRING_RULE,
    "evaluation_run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_OBJECT_RULE,
}
