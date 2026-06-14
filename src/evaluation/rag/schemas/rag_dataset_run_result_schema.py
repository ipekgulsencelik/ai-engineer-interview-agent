from __future__ import annotations

from datetime import datetime

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)
from src.domain.validation.schema_rules import ValidationRule

DATETIME_OBJECT_RULE = ValidationRule(expected_type=datetime)


RAG_DATASET_RUN_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "retriever_name": NON_EMPTY_STRING_RULE,
    "evaluator_name": NON_EMPTY_STRING_RULE,
    "sample_count": NON_NEGATIVE_NUMBER_RULE,
    "passed_count": NON_NEGATIVE_NUMBER_RULE,
    "failed_count": NON_NEGATIVE_NUMBER_RULE,
    "pass_rate": RATIO_RULE,
    "overall_score": RATIO_RULE,
    "started_at": DATETIME_OBJECT_RULE,
    "completed_at": DATETIME_OBJECT_RULE,
    "duration_ms": NON_NEGATIVE_NUMBER_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}