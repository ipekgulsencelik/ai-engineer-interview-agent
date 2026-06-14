from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_NUMBER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


WORKER_NODE_SCHEMA: Final[
    SchemaDefinition
] = {
    "node_id": NON_EMPTY_STRING_RULE,
    "worker_id": NON_EMPTY_STRING_RULE,
    "worker_name": NON_EMPTY_STRING_RULE,
    "hostname": NON_EMPTY_STRING_RULE,
    "region": NON_EMPTY_STRING_RULE,
    "status": NON_EMPTY_STRING_RULE,
    "started_at": DATETIME_RULE,
    "last_heartbeat_at": DATETIME_RULE,
    "queue_name": OPTIONAL_STRING_RULE,
    "current_job_id": OPTIONAL_STRING_RULE,
    "processed_job_count": NON_NEGATIVE_NUMBER_RULE,
    "failed_job_count": NON_NEGATIVE_NUMBER_RULE,
    "max_concurrency": POSITIVE_NUMBER_RULE,
    "metadata": DICT_RULE,
    "notes": OPTIONAL_STRING_RULE,
}