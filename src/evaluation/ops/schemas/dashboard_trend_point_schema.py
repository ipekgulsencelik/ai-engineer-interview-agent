from __future__ import annotations

from datetime import datetime
from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_rules import ValidationRule
from src.domain.validation.schema_types import SchemaDefinition

DATETIME_OBJECT_RULE: Final[ValidationRule] = ValidationRule(expected_type=datetime)

DASHBOARD_TREND_POINT_SCHEMA: Final[SchemaDefinition] = {
    "point_id": NON_EMPTY_STRING_RULE,
    "metric_name": NON_EMPTY_STRING_RULE,
    "value": NUMBER_RULE,
    "occurred_at": DATETIME_OBJECT_RULE,
    "unit": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "label": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}
