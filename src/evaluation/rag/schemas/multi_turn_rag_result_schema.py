from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


MULTI_TURN_RAG_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "conversation_id": NON_EMPTY_STRING_RULE,
    "turn_results": TUPLE_RULE,
    "average_faithfulness_score": RATIO_RULE,
    "average_answer_relevancy_score": RATIO_RULE,
    "average_context_precision_score": RATIO_RULE,
    "overall_score": RATIO_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}