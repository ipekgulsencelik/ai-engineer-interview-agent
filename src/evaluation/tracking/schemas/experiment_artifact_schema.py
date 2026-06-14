from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_ARTIFACT_SCHEMA: Final[
    SchemaDefinition
] = {
    "artifact_id": NON_EMPTY_STRING_RULE,
    "run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "artifact_type": NON_EMPTY_STRING_RULE,
    "artifact_name": NON_EMPTY_STRING_RULE,
    "artifact_path": NON_EMPTY_STRING_RULE,
    "artifact_uri": OPTIONAL_STRING_RULE,
    "storage_backend": OPTIONAL_STRING_RULE,
    "content_type": NON_EMPTY_STRING_RULE,
    "size_bytes": OPTIONAL_NUMBER_RULE,
    "checksum": OPTIONAL_STRING_RULE,
    "created_at": DATETIME_RULE,
    "description": OPTIONAL_STRING_RULE,
    "tags": TUPLE_RULE,
    "metadata": DICT_RULE,
}