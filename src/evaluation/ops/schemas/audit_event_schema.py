from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


AUDIT_EVENT_SCHEMA: Final[
    SchemaDefinition
] = {
    "event_id": NON_EMPTY_STRING_RULE,
    "aggregate_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "occurred_at": DATETIME_RULE,
    "actor": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}