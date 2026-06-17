from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


TELEMETRY_METRIC_SCHEMA: Final[
    SchemaDefinition
] = {
    "metric_id": NON_EMPTY_STRING_RULE,
    "metric_name": NON_EMPTY_STRING_RULE,
    "metric_value": NON_EMPTY_STRING_RULE,
    "unit": NON_EMPTY_STRING_RULE,
    "source": NON_EMPTY_STRING_RULE,
    "recorded_at": DATETIME_RULE,
    "labels": DICT_RULE,
    "tenant_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "report_id": OPTIONAL_STRING_RULE,
    "artifact_id": OPTIONAL_STRING_RULE,
    "worker_id": OPTIONAL_STRING_RULE,
    "correlation_id": OPTIONAL_STRING_RULE,
    "trace_id": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}