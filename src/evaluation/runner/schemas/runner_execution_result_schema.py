from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


RUNNER_EXECUTION_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "execution_id": NON_EMPTY_STRING_RULE,
    "runner_id": NON_EMPTY_STRING_RULE,
    "runner_name": NON_EMPTY_STRING_RULE,
    "status": NON_EMPTY_STRING_RULE,
    "started_at": DATETIME_RULE,
    "completed_at": DATETIME_RULE,
    "duration_ms": OPTIONAL_NUMBER_RULE,
    "success": BOOLEAN_RULE,
    "score": OPTIONAL_NUMBER_RULE,
    "error_message": OPTIONAL_STRING_RULE,
    "retry_count": NON_NEGATIVE_NUMBER_RULE,
    "output_uri": OPTIONAL_STRING_RULE,
    "artifact_id": OPTIONAL_STRING_RULE,
    "report_id": OPTIONAL_STRING_RULE,
    "dataset_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "worker_id": OPTIONAL_STRING_RULE,
    "correlation_id": OPTIONAL_STRING_RULE,
    "trace_id": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}