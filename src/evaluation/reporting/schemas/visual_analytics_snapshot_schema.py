from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


VISUAL_ANALYTICS_SNAPSHOT_SCHEMA: Final[
    SchemaDefinition
] = {
    "snapshot_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "chart_type": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "labels": TUPLE_RULE,
    "scores": TUPLE_RULE,
    "average_score": OPTIONAL_RATIO_RULE,
    "trend_direction": OPTIONAL_STRING_RULE,
    "x_axis_label": OPTIONAL_STRING_RULE,
    "y_axis_label": OPTIONAL_STRING_RULE,
    "series_name": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}