from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EVALUATION_AUDIT_TRAIL_SCHEMA: Final[
    SchemaDefinition
] = {
    "trail_id": NON_EMPTY_STRING_RULE,
    "evaluation_run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
}