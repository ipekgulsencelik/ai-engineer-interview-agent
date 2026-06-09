from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


TREND_VISUALIZATION_SNAPSHOT_SCHEMA: Final[SchemaDefinition] = {
    "title": NON_EMPTY_STRING_RULE,
    "description": NON_EMPTY_STRING_RULE,
    "trend_direction": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}