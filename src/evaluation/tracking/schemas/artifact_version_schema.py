from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


ARTIFACT_VERSION_SCHEMA: Final[
    SchemaDefinition
] = {
    "version_id": NON_EMPTY_STRING_RULE,
    "artifact_id": NON_EMPTY_STRING_RULE,
    "version": NON_EMPTY_STRING_RULE,
    "path": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "artifact_uri": OPTIONAL_STRING_RULE,
    "checksum": OPTIONAL_STRING_RULE,
    "size_bytes": OPTIONAL_NUMBER_RULE,
    "created_by": OPTIONAL_STRING_RULE,
    "change_summary": OPTIONAL_STRING_RULE,
    "parent_version_id": OPTIONAL_STRING_RULE,
    "metadata": DICT_RULE,
}