from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_INTEGER_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BENCHMARK_AGGREGATE_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "experiment_count": POSITIVE_INTEGER_RULE,
    "mean_score": RATIO_RULE,
    "median_score": RATIO_RULE,
    "min_score": RATIO_RULE,
    "max_score": RATIO_RULE,
    "std_deviation": NON_NEGATIVE_NUMBER_RULE,
    "trend_direction": NON_EMPTY_STRING_RULE,
    "best_experiment_id": NON_EMPTY_STRING_RULE,
    "worst_experiment_id": NON_EMPTY_STRING_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}