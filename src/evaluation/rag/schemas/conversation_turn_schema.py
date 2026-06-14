from __future__ import annotations

from datetime import datetime

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)
from src.domain.validation.schema_rules import ValidationRule

DATETIME_OBJECT_RULE = ValidationRule(expected_type=datetime)


CONVERSATION_TURN_SCHEMA: Final[
    SchemaDefinition
] = {
    "turn_id": NON_EMPTY_STRING_RULE,
    "conversation_id": NON_EMPTY_STRING_RULE,
    "turn_index": NON_NEGATIVE_NUMBER_RULE,
    "user_message": NON_EMPTY_STRING_RULE,
    "assistant_message": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_OBJECT_RULE,
    "retrieved_context": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "retriever_name": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}