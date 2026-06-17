from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BENCHMARK_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "result_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "started_at": DATETIME_RULE,
    "completed_at": DATETIME_RULE,
    "overall_score": OPTIONAL_NUMBER_RULE,
    "passed": BOOLEAN_RULE,
    "sample_count": NON_NEGATIVE_NUMBER_RULE,
    "passed_count": NON_NEGATIVE_NUMBER_RULE,
    "failed_count": NON_NEGATIVE_NUMBER_RULE,
    "duration_ms": OPTIONAL_NUMBER_RULE,
    "pass_rate": OPTIONAL_NUMBER_RULE,
    "average_score": OPTIONAL_NUMBER_RULE,
    "best_score": OPTIONAL_NUMBER_RULE,
    "worst_score": OPTIONAL_NUMBER_RULE,
    "evaluator_name": OPTIONAL_STRING_RULE,
    "dataset_id": OPTIONAL_STRING_RULE,
    "dataset_name": OPTIONAL_STRING_RULE,
    "dataset_version": OPTIONAL_STRING_RULE,
    "tenant_id": OPTIONAL_STRING_RULE,
    "baseline_run_id": OPTIONAL_STRING_RULE,
    "candidate_run_id": OPTIONAL_STRING_RULE,
    "score_delta": OPTIONAL_NUMBER_RULE,
    "winner": OPTIONAL_STRING_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}