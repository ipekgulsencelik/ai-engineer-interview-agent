from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_INTEGER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import SchemaDefinition


RETRIEVED_CHUNK_SCHEMA: Final[SchemaDefinition] = {
    "chunk_id": NON_EMPTY_STRING_RULE,
    "chunk_text": NON_EMPTY_STRING_RULE,
    "document_id": OPTIONAL_STRING_RULE,
    "source_name": OPTIONAL_STRING_RULE,
    "rank": OPTIONAL_INTEGER_RULE,
    "score": OPTIONAL_NUMBER_RULE,
}
