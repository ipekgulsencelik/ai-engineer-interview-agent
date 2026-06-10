from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BENCHMARK_EVALUATION_REPORT_SCHEMA: Final[SchemaDefinition] = {
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "dataset_id": NON_EMPTY_STRING_RULE,
    "dataset_version": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "evaluator_id": NON_EMPTY_STRING_RULE,
    "overall_score": RATIO_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}