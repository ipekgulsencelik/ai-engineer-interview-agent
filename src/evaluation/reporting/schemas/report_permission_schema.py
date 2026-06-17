from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REPORT_PERMISSION_SCHEMA: Final[
    SchemaDefinition
] = {
    "permission_id": NON_EMPTY_STRING_RULE,
    "report_id": NON_EMPTY_STRING_RULE,
    "principal_id": NON_EMPTY_STRING_RULE,
    "principal_type": NON_EMPTY_STRING_RULE,
    "role": OPTIONAL_STRING_RULE,
    "action": NON_EMPTY_STRING_RULE,
    "granted": BOOLEAN_RULE,
    "created_at": DATETIME_RULE,
    "created_by": NON_EMPTY_STRING_RULE,
    "tenant_id": OPTIONAL_STRING_RULE,
    "resource_type": NON_EMPTY_STRING_RULE,
    "expires_at": DATETIME_RULE,
    "reason": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}