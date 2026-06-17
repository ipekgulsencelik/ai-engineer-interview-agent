from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    POSITIVE_NUMBER_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DASHBOARD_LAYOUT_SCHEMA: Final[
    SchemaDefinition
] = {
    "layout_id": NON_EMPTY_STRING_RULE,
    "dashboard_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "widgets": TUPLE_RULE,
    "columns": POSITIVE_NUMBER_RULE,
    "row_height": POSITIVE_NUMBER_RULE,
    "gap": NON_NEGATIVE_NUMBER_RULE,
    "compact": BOOLEAN_RULE,
    "responsive": BOOLEAN_RULE,
    "metadata": DICT_RULE,
}