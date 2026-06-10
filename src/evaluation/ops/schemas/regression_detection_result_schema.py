from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REGRESSION_DETECTION_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "baseline_experiment_id": (
        NON_EMPTY_STRING_RULE
    ),
    "candidate_experiment_id": (
        NON_EMPTY_STRING_RULE
    ),
    "baseline_score": RATIO_RULE,
    "candidate_score": RATIO_RULE,
    "score_delta": NUMBER_RULE,
    "regression_threshold": (
        NON_NEGATIVE_NUMBER_RULE
    ),
    "regression_detected": BOOLEAN_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}