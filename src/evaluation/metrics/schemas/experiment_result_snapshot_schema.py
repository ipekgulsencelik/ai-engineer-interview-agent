from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_RESULT_SNAPSHOT_SCHEMA: Final[SchemaDefinition] = {
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "dataset_id": NON_EMPTY_STRING_RULE,
    "dataset_version": NON_EMPTY_STRING_RULE,
    "dataset_hash": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "metrics_version": NON_EMPTY_STRING_RULE,
    "execution_time_seconds": NON_NEGATIVE_NUMBER_RULE,
    "tags": STRING_TUPLE_RULE,
    "notes": OPTIONAL_STRING_RULE,
}