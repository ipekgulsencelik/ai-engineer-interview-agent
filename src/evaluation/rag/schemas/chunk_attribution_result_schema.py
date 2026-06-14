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


CHUNK_ATTRIBUTION_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "chunk_id": NON_EMPTY_STRING_RULE,
    "attribution_score": RATIO_RULE,
    "supports_answer": BOOLEAN_RULE,
    "chunk_token_count": NON_NEGATIVE_NUMBER_RULE,
    "matched_tokens": NON_NEGATIVE_NUMBER_RULE,
    "document_id": OPTIONAL_STRING_RULE,
    "source_name": OPTIONAL_STRING_RULE,
    "matched_text": OPTIONAL_STRING_RULE,
    "explanation": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}