from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


PRODUCTION_EVALUATION_DASHBOARD_SCHEMA: Final[
    SchemaDefinition
] = {
    "dashboard_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "generated_at": DATETIME_RULE,
    "notes": OPTIONAL_STRING_RULE,
}