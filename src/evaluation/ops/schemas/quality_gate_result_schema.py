from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


QUALITY_GATE_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "gate_name": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "metric_name": NON_EMPTY_STRING_RULE,
    "actual_value": NUMBER_RULE,
    "expected_value": NUMBER_RULE,
    "overall_score": RATIO_RULE,
    "minimum_required_score": RATIO_RULE,
    "passed": BOOLEAN_RULE,
    "severity": NON_EMPTY_STRING_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}