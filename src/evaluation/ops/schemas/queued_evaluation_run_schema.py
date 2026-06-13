from __future__ import annotations

from typing import Final
from datetime import datetime

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
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

OPTIONAL_DATETIME_OBJECT_RULE: Final[ValidationRule] = ValidationRule(
    expected_type=datetime,
    nullable=True,
)


QUEUED_EVALUATION_RUN_SCHEMA: Final[SchemaDefinition] = {
    "queue_id": NON_EMPTY_STRING_RULE,
    "run_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "priority": NON_NEGATIVE_NUMBER_RULE,
    "requested_by": NON_EMPTY_STRING_RULE,
    "queued_at": DATETIME_OBJECT_RULE,
    "scheduled_at": OPTIONAL_DATETIME_OBJECT_RULE,
    "notes": OPTIONAL_STRING_RULE,
}
