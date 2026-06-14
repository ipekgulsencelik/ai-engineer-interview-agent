from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_RUN_SCHEMA: Final[
    SchemaDefinition
] = {
    "run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "experiment_name": NON_EMPTY_STRING_RULE,
    "experiment_version": NON_EMPTY_STRING_RULE,
    "started_at": DATETIME_RULE,
    "status": NON_EMPTY_STRING_RULE,
    "dataset_id": OPTIONAL_STRING_RULE,
    "dataset_name": OPTIONAL_STRING_RULE,
    "dataset_version": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "benchmark_name": OPTIONAL_STRING_RULE,
    "benchmark_version": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "retriever_name": OPTIONAL_STRING_RULE,
    "evaluator_name": OPTIONAL_STRING_RULE,
    "overall_score": OPTIONAL_RATIO_RULE,
    "pass_rate": OPTIONAL_RATIO_RULE,
    "sample_count": OPTIONAL_NUMBER_RULE,
    "passed_count": OPTIONAL_NUMBER_RULE,
    "failed_count": OPTIONAL_NUMBER_RULE,
    "completed_at": DATETIME_RULE,
    "duration_ms": OPTIONAL_NUMBER_RULE,
    "notes": OPTIONAL_STRING_RULE,
}