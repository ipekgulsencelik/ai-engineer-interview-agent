from __future__ import annotations

from datetime import datetime
from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_rules import ValidationRule
from src.domain.validation.schema_types import SchemaDefinition

DATETIME_OBJECT_RULE: Final[ValidationRule] = ValidationRule(expected_type=datetime)

PRODUCTION_EVALUATION_DASHBOARD_SCHEMA: Final[SchemaDefinition] = {
    "dashboard_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "generated_at": DATETIME_OBJECT_RULE,
    "notes": OPTIONAL_STRING_RULE,
}
