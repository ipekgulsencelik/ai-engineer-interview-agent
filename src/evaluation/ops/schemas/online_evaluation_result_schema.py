from __future__ import annotations

from typing import Final
from datetime import datetime

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    NUMBER_RULE,
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


ONLINE_EVALUATION_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "result_id": NON_EMPTY_STRING_RULE,
    "request_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "evaluator_name": NON_EMPTY_STRING_RULE,
    "metric_name": NON_EMPTY_STRING_RULE,
    "metric_value": NUMBER_RULE,
    "passed": BOOLEAN_RULE,
    "latency_ms": NON_NEGATIVE_NUMBER_RULE,
    "created_at": DATETIME_OBJECT_RULE,
    "session_id": OPTIONAL_STRING_RULE,
    "user_id": OPTIONAL_STRING_RULE,
    "trace_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "interpretation": OPTIONAL_STRING_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}
