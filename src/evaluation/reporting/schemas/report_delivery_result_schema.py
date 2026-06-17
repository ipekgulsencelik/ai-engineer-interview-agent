from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REPORT_DELIVERY_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "delivery_id": NON_EMPTY_STRING_RULE,
    "report_id": NON_EMPTY_STRING_RULE,
    "artifact_id": NON_EMPTY_STRING_RULE,
    "delivery_type": NON_EMPTY_STRING_RULE,
    "destination": NON_EMPTY_STRING_RULE,
    "success": BOOLEAN_RULE,
    "delivered_at": DATETIME_RULE,
    "provider": OPTIONAL_STRING_RULE,
    "status_code": OPTIONAL_NUMBER_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "retry_count": NON_NEGATIVE_NUMBER_RULE,
    "metadata": DICT_RULE,
}