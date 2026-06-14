from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    POSITIVE_INTEGER_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_TREND_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "experiment_id": NON_EMPTY_STRING_RULE,
    "experiment_name": NON_EMPTY_STRING_RULE,
    "experiment_version": NON_EMPTY_STRING_RULE,
    "run_count": POSITIVE_INTEGER_RULE,
    "first_run_id": NON_EMPTY_STRING_RULE,
    "latest_run_id": NON_EMPTY_STRING_RULE,
    "first_overall_score": OPTIONAL_RATIO_RULE,
    "latest_overall_score": OPTIONAL_RATIO_RULE,
    "average_overall_score": OPTIONAL_RATIO_RULE,
    "overall_score_delta": OPTIONAL_NUMBER_RULE,
    "first_pass_rate": OPTIONAL_RATIO_RULE,
    "latest_pass_rate": OPTIONAL_RATIO_RULE,
    "pass_rate_delta": OPTIONAL_NUMBER_RULE,
    "best_run_id": OPTIONAL_STRING_RULE,
    "best_overall_score": OPTIONAL_RATIO_RULE,
    "worst_run_id": OPTIONAL_STRING_RULE,
    "worst_overall_score": OPTIONAL_RATIO_RULE,
    "trend_direction": NON_EMPTY_STRING_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}