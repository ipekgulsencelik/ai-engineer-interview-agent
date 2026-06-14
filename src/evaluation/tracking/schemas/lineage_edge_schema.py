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


LINEAGE_EDGE_SCHEMA: Final[
    SchemaDefinition
] = {
    "edge_id": NON_EMPTY_STRING_RULE,
    "parent_id": NON_EMPTY_STRING_RULE,
    "child_id": NON_EMPTY_STRING_RULE,
    "relationship_type": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "description": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}