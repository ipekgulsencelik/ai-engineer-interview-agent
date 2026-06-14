from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


SEMANTIC_SIMILARITY_REQUEST_SCHEMA: Final[
    SchemaDefinition
] = {
    "reference_text": NON_EMPTY_STRING_RULE,
    "candidate_text": NON_EMPTY_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "evaluator_name": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}