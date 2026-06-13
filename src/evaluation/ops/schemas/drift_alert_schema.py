from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DRIFT_ALERT_SCHEMA: Final[
    SchemaDefinition
] = {
    "alert_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "baseline_score": NUMBER_RULE,
    "current_score": NUMBER_RULE,
    "drift_delta": NUMBER_RULE,
    "drift_threshold": NUMBER_RULE,
    "alert_triggered": BOOLEAN_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "acknowledged": BOOLEAN_RULE,
    "acknowledged_by": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}