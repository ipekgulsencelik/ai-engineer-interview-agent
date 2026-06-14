from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


RAG_EVALUATION_SAMPLE_SCHEMA: Final[
    SchemaDefinition
] = {
    "sample_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "question": NON_EMPTY_STRING_RULE,
    "expected_answer": OPTIONAL_STRING_RULE,
    "expected_context": OPTIONAL_STRING_RULE,
    "expected_chunk_ids": TUPLE_RULE,
    "metadata": DICT_RULE,
    "tags": TUPLE_RULE,
    "difficulty": OPTIONAL_STRING_RULE,
    "category": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}