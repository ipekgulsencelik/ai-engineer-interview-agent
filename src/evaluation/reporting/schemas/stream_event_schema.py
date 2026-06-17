from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


STREAM_EVENT_SCHEMA: Final[
    SchemaDefinition
] = {
    "event_id": NON_EMPTY_STRING_RULE,
    "stream_id": NON_EMPTY_STRING_RULE,
    "event_type": NON_EMPTY_STRING_RULE,
    "occurred_at": DATETIME_RULE,
    "source": NON_EMPTY_STRING_RULE,
    "sequence_number": NON_NEGATIVE_NUMBER_RULE,
    "payload": DICT_RULE,
    "correlation_id": OPTIONAL_STRING_RULE,
    "trace_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "entity_type": OPTIONAL_STRING_RULE,
    "entity_id": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}