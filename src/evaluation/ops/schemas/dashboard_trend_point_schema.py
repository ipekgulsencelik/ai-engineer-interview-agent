from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DASHBOARD_TREND_POINT_SCHEMA: Final[
    SchemaDefinition
] = {
    "point_id": NON_EMPTY_STRING_RULE,
    "metric_name": NON_EMPTY_STRING_RULE,
    "value": NUMBER_RULE,
    "occurred_at": DATETIME_RULE,
    "unit": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "label": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}