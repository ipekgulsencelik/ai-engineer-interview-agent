from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_NEGATIVE_NUMBER_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


TURN_RAG_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "turn_index": NON_NEGATIVE_NUMBER_RULE,
    "faithfulness_score": RATIO_RULE,
    "answer_relevancy_score": RATIO_RULE,
    "context_precision_score": RATIO_RULE,
    "overall_score": RATIO_RULE,
}