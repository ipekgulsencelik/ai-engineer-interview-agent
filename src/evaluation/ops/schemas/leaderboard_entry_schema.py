from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_INTEGER_RULE,
    RATIO_RULE,
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


LEADERBOARD_ENTRY_SCHEMA: Final[SchemaDefinition] = {
    "rank": POSITIVE_INTEGER_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "overall_score": RATIO_RULE,
    "dataset_id": NON_EMPTY_STRING_RULE,
    "dataset_version": NON_EMPTY_STRING_RULE,
    "dataset_hash": NON_EMPTY_STRING_RULE,
    "metrics_version": NON_EMPTY_STRING_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "tags": STRING_TUPLE_RULE,
    "notes": OPTIONAL_STRING_RULE,
}