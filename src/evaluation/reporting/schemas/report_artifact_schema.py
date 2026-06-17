from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
    OPTIONAL_TUPLE_RULE,
    OPTIONAL_DICT_RULE,
    OPTIONAL_NON_NEGATIVE_NUMBER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REPORT_ARTIFACT_SCHEMA: Final[
    SchemaDefinition
] = {
    "report_id": NON_EMPTY_STRING_RULE,
    "artifact_id": NON_EMPTY_STRING_RULE,
    "run_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "report_type": NON_EMPTY_STRING_RULE,
    "artifact_type": NON_EMPTY_STRING_RULE,
    "path": NON_EMPTY_STRING_RULE,
    "content": OPTIONAL_STRING_RULE,
    "uri": OPTIONAL_STRING_RULE,
    "storage_backend": OPTIONAL_STRING_RULE,
    "format": OPTIONAL_STRING_RULE,
    "content_type": NON_EMPTY_STRING_RULE,
    "size_bytes": OPTIONAL_NON_NEGATIVE_NUMBER_RULE,
    "checksum": OPTIONAL_STRING_RULE,
    "generated_by": OPTIONAL_STRING_RULE,
    "created_at": DATETIME_RULE,
    "description": OPTIONAL_STRING_RULE,
    "tags": OPTIONAL_TUPLE_RULE,
    "metadata": OPTIONAL_DICT_RULE,
}