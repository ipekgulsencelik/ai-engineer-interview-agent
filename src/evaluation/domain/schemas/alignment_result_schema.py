from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    CORRELATION_RULE,
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    PERCENTAGE_RULE,
    SEMVER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


ALIGNMENT_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "sample_id": NON_EMPTY_STRING_RULE,

    "alignment_evaluation_id": NON_EMPTY_STRING_RULE,
    "alignment_evaluation_timestamp": DATETIME_RULE,
    "alignment_evaluation_version": SEMVER_RULE,
    "alignment_evaluation_criteria": NON_EMPTY_STRING_RULE,
    "alignment_evaluation_feedback": NON_EMPTY_STRING_RULE,

    "pearson_correlation": CORRELATION_RULE,
    "cohen_kappa": CORRELATION_RULE,
    "mean_absolute_error": NON_NEGATIVE_NUMBER_RULE,

    "llm_model_name": NON_EMPTY_STRING_RULE,
    "human_evaluator_id": NON_EMPTY_STRING_RULE,

    "overall_alignment_score": PERCENTAGE_RULE,
    "technical_alignment_score": PERCENTAGE_RULE,
    "communication_alignment_score": PERCENTAGE_RULE,
    "reasoning_alignment_score": PERCENTAGE_RULE,
}