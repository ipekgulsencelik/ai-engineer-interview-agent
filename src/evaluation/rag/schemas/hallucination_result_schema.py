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


HALLUCINATION_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "label": NON_EMPTY_STRING_RULE,
    "confidence": RATIO_RULE,
    "hallucination_score": RATIO_RULE,
    "hallucination_detected": BOOLEAN_RULE,
    "unsupported_claim_count": NON_NEGATIVE_NUMBER_RULE,
    "total_claim_count": NON_NEGATIVE_NUMBER_RULE,
    "explanation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}