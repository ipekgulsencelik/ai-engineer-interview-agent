from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)

CI_BENCHMARK_POLICY_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "policy_name": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "benchmark_score": RATIO_RULE,
    "minimum_required_score": RATIO_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "overall_score": RATIO_RULE,
    "deployment_allowed": BOOLEAN_RULE,
    "blocking_failure_count": (
        NON_NEGATIVE_NUMBER_RULE
    ),
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}