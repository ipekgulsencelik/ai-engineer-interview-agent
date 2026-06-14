from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_QUERY_SCHEMA: Final[
    SchemaDefinition
] = {
    "experiment_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "experiment_name": OPTIONAL_STRING_RULE,
    "experiment_version": OPTIONAL_STRING_RULE,
    "dataset_id": OPTIONAL_STRING_RULE,
    "dataset_name": OPTIONAL_STRING_RULE,
    "dataset_version": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "benchmark_name": OPTIONAL_STRING_RULE,
    "benchmark_version": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "retriever_name": OPTIONAL_STRING_RULE,
    "evaluator_name": OPTIONAL_STRING_RULE,
    "status": OPTIONAL_STRING_RULE,
    "tag_key": OPTIONAL_STRING_RULE,
    "tag_value": OPTIONAL_STRING_RULE,
    "created_after": DATETIME_RULE,
    "created_before": DATETIME_RULE,
    "min_overall_score": OPTIONAL_RATIO_RULE,
    "max_overall_score": OPTIONAL_RATIO_RULE,
    "min_pass_rate": OPTIONAL_RATIO_RULE,
    "max_pass_rate": OPTIONAL_RATIO_RULE,
    "limit": OPTIONAL_NUMBER_RULE,
    "offset": OPTIONAL_NUMBER_RULE,
}