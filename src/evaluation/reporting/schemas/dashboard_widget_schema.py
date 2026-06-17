from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_NUMBER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DASHBOARD_WIDGET_SCHEMA: Final[
    SchemaDefinition
] = {
    "widget_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "widget_type": NON_EMPTY_STRING_RULE,
    "data": DICT_RULE,
    "payload": DICT_RULE,
    "order": NON_NEGATIVE_NUMBER_RULE,
    "width": POSITIVE_NUMBER_RULE,
    "height": POSITIVE_NUMBER_RULE,
    "description": OPTIONAL_STRING_RULE,
    "group": OPTIONAL_STRING_RULE,
    "refresh_interval_seconds": OPTIONAL_NUMBER_RULE,
    "metadata": DICT_RULE,
}