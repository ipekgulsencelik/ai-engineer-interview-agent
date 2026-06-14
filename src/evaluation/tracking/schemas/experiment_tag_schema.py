from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_TAG_SCHEMA: Final[
    SchemaDefinition
] = {
    "tag_id": NON_EMPTY_STRING_RULE,
    "key": NON_EMPTY_STRING_RULE,
    "value": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "description": OPTIONAL_STRING_RULE,
    "created_by": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}