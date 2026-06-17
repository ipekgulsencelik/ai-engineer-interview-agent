from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


CHART_DATA_SCHEMA: Final[
    SchemaDefinition
] = {
    "title": NON_EMPTY_STRING_RULE,
    "chart_type": NON_EMPTY_STRING_RULE,
    "labels": TUPLE_RULE,
    "scores": TUPLE_RULE,
    "average_score": OPTIONAL_RATIO_RULE,
    "trend_direction": OPTIONAL_STRING_RULE,
    "x_axis_label": OPTIONAL_STRING_RULE,
    "y_axis_label": OPTIONAL_STRING_RULE,
    "series_name": OPTIONAL_STRING_RULE,
    "metric_name": OPTIONAL_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}