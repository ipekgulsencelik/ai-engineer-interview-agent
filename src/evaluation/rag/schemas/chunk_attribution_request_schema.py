from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


CHUNK_ATTRIBUTION_REQUEST_SCHEMA: Final[
    SchemaDefinition
] = {
    "question": NON_EMPTY_STRING_RULE,
    "generated_answer": NON_EMPTY_STRING_RULE,
    "retrieved_chunks": TUPLE_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "evaluator_name": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}