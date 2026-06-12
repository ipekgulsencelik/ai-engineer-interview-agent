from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_BOOLEAN_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DASHBOARD_METRIC_CARD_SCHEMA: Final[
    SchemaDefinition
] = {
    "card_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "value": NON_NEGATIVE_NUMBER_RULE,
    "formatted_value": (
        NON_EMPTY_STRING_RULE
    ),
    "unit": OPTIONAL_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "trend_value": OPTIONAL_NUMBER_RULE,
    "trend_label": OPTIONAL_STRING_RULE,
    "is_positive_trend": (
        OPTIONAL_BOOLEAN_RULE
    ),
    "severity": OPTIONAL_STRING_RULE,
    "sort_order": (
        NON_NEGATIVE_NUMBER_RULE
    ),
}