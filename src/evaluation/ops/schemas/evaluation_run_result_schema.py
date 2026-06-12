from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EVALUATION_RUN_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "run_id": NON_EMPTY_STRING_RULE,
    "started_at": DATETIME_RULE,
    "completed_at": DATETIME_RULE,
    "duration_seconds": (
        NON_NEGATIVE_NUMBER_RULE
    ),
    "success": BOOLEAN_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}