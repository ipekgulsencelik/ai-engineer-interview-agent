from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    PERCENTAGE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


LLM_SCORE_SCHEMA: Final[SchemaDefinition] = {
    "sample_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "overall_score": PERCENTAGE_RULE,
    "technical_score": PERCENTAGE_RULE,
    "communication_score": PERCENTAGE_RULE,
    "reasoning_score": PERCENTAGE_RULE,
    "confidence_score": PERCENTAGE_RULE,
    "feedback": NON_EMPTY_STRING_RULE,
}