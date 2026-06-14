from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
    NON_EMPTY_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


MULTI_TURN_RAG_REQUEST_SCHEMA: Final[
    SchemaDefinition
] = {
    "conversation_id": NON_EMPTY_STRING_RULE,
    "turns": TUPLE_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "retriever_name": OPTIONAL_STRING_RULE,
    "evaluator_name": OPTIONAL_STRING_RULE,
    "expected_answer": OPTIONAL_STRING_RULE,
    "expected_conversation_outcome": (
        OPTIONAL_STRING_RULE
    ),
    "notes": OPTIONAL_STRING_RULE,
}