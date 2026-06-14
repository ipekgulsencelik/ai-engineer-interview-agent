from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_COMPARISON_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "baseline_run_id": NON_EMPTY_STRING_RULE,
    "candidate_run_id": NON_EMPTY_STRING_RULE,
    "baseline_experiment_id": NON_EMPTY_STRING_RULE,
    "candidate_experiment_id": NON_EMPTY_STRING_RULE,
    "baseline_experiment_name": NON_EMPTY_STRING_RULE,
    "candidate_experiment_name": NON_EMPTY_STRING_RULE,
    "baseline_experiment_version": NON_EMPTY_STRING_RULE,
    "candidate_experiment_version": NON_EMPTY_STRING_RULE,
    "baseline_overall_score": OPTIONAL_RATIO_RULE,
    "candidate_overall_score": OPTIONAL_RATIO_RULE,
    "overall_score_delta": OPTIONAL_NUMBER_RULE,
    "baseline_pass_rate": OPTIONAL_RATIO_RULE,
    "candidate_pass_rate": OPTIONAL_RATIO_RULE,
    "pass_rate_delta": OPTIONAL_NUMBER_RULE,
    "baseline_sample_count": OPTIONAL_NUMBER_RULE,
    "candidate_sample_count": OPTIONAL_NUMBER_RULE,
    "sample_count_delta": OPTIONAL_NUMBER_RULE,
    "winner_experiment_id": OPTIONAL_STRING_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}