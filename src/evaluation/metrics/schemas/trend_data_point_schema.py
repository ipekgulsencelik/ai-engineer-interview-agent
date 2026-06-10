from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NUMBER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


TREND_DATA_POINT_SCHEMA: Final[SchemaDefinition] = {
    "label": NON_EMPTY_STRING_RULE,
    "value": NUMBER_RULE,
}