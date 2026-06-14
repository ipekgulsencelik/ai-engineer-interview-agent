from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


MODEL_REGISTRY_ENTRY_SCHEMA: Final[
    SchemaDefinition
] = {
    "registry_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "model_version": NON_EMPTY_STRING_RULE,
    "stage": NON_EMPTY_STRING_RULE,
    "created_at": DATETIME_RULE,
    "framework": OPTIONAL_STRING_RULE,
    "provider": OPTIONAL_STRING_RULE,
    "model_uri": OPTIONAL_STRING_RULE,
    "artifact_path": OPTIONAL_STRING_RULE,
    "checksum": OPTIONAL_STRING_RULE,
    "owner": OPTIONAL_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "tags": TUPLE_RULE,
    "metadata": DICT_RULE,
    "benchmark_score": OPTIONAL_RATIO_RULE,
}