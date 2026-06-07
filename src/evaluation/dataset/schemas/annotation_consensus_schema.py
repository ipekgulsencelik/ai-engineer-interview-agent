from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    CORRELATION_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    PERCENTAGE_RULE,
    POSITIVE_INTEGER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


ANNOTATION_CONSENSUS_SCHEMA: Final[SchemaDefinition] = {
    "evaluation_id": NON_EMPTY_STRING_RULE,
    "evaluator_count": POSITIVE_INTEGER_RULE,
    "sample_count": POSITIVE_INTEGER_RULE,
    "agreement_score": PERCENTAGE_RULE,
    "cohen_kappa": CORRELATION_RULE,
    "fleiss_kappa": CORRELATION_RULE,
    "mean_score_variance": NON_NEGATIVE_NUMBER_RULE,
    "notes": OPTIONAL_STRING_RULE,
}