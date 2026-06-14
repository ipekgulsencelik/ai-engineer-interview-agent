from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


RETRIEVAL_HIT_RATE_REQUEST_SCHEMA: Final[
    SchemaDefinition
] = {
    "question": NON_EMPTY_STRING_RULE,
    "expected_chunk_id": NON_EMPTY_STRING_RULE,
    "retrieved_chunk_ids": TUPLE_RULE,
    "top_k": NON_NEGATIVE_NUMBER_RULE,
    "expected_context": OPTIONAL_STRING_RULE,
    "retrieved_contexts": TUPLE_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "retriever_name": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}