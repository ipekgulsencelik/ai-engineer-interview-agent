from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    METADATA_RULE,
    NON_EMPTY_STRING_RULE,
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EVALUATION_SAMPLE_SCHEMA: Final[SchemaDefinition] = {
    "sample_id": NON_EMPTY_STRING_RULE,
    "question_id": NON_EMPTY_STRING_RULE,
    "question": NON_EMPTY_STRING_RULE,
    "candidate_answer": NON_EMPTY_STRING_RULE,
    "expected_answer": NON_EMPTY_STRING_RULE,
    "category": NON_EMPTY_STRING_RULE,
    "retrieved_contexts": STRING_TUPLE_RULE,
    "metadata": METADATA_RULE,
}