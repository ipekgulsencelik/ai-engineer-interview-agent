from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_DICT_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import SchemaDefinition

REPORT_TEMPLATE_SCHEMA: Final[SchemaDefinition] = {
    "template_id": NON_EMPTY_STRING_RULE,
    "name": NON_EMPTY_STRING_RULE,
    "report_type": NON_EMPTY_STRING_RULE,
    "template_format": NON_EMPTY_STRING_RULE,
    "template_content": NON_EMPTY_STRING_RULE,
    "version": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "created_by": NON_EMPTY_STRING_RULE,
    "title": OPTIONAL_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "enabled": BOOLEAN_RULE,
    "tags": TUPLE_RULE,
    "variables": TUPLE_RULE,
    "metadata": OPTIONAL_DICT_RULE,
}
