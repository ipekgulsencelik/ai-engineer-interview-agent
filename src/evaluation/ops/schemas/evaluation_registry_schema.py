from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EVALUATION_REGISTRY_SCHEMA: Final[SchemaDefinition] = {
    "registry_id": NON_EMPTY_STRING_RULE,
    "registry_name": NON_EMPTY_STRING_RULE,
    "version": NON_EMPTY_STRING_RULE,
    "is_locked": BOOLEAN_RULE,
    "notes": OPTIONAL_STRING_RULE,
}