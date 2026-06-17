from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


SCHEDULED_REPORT_SCHEMA: Final[
    SchemaDefinition
] = {
    "schedule_id": NON_EMPTY_STRING_RULE,
    "report_id": NON_EMPTY_STRING_RULE,
    "report_name": NON_EMPTY_STRING_RULE,
    "report_type": NON_EMPTY_STRING_RULE,
    "report_format": NON_EMPTY_STRING_RULE,
    "cron_expression": NON_EMPTY_STRING_RULE,
    "output_directory": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "enabled": BOOLEAN_RULE,
    "dashboard_id": OPTIONAL_STRING_RULE,
    "experiment_id": OPTIONAL_STRING_RULE,
    "run_id": OPTIONAL_STRING_RULE,
    "benchmark_id": OPTIONAL_STRING_RULE,
    "model_name": OPTIONAL_STRING_RULE,
    "generated_by": OPTIONAL_STRING_RULE,
    "last_run_at": DATETIME_RULE,
    "next_run_at": DATETIME_RULE,
    "execution_count": NON_NEGATIVE_NUMBER_RULE,
    "failure_count": NON_NEGATIVE_NUMBER_RULE,
    "last_error": OPTIONAL_STRING_RULE,
    "recipient_emails": TUPLE_RULE,
    "metadata": DICT_RULE,
    "notes": OPTIONAL_STRING_RULE,
}