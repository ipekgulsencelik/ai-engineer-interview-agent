from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REGISTERED_BENCHMARK_SCHEMA: Final[SchemaDefinition] = {
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "name": NON_EMPTY_STRING_RULE,
    "version": NON_EMPTY_STRING_RULE,
    "dataset_id": NON_EMPTY_STRING_RULE,
    "dataset_version": NON_EMPTY_STRING_RULE,
    "description": OPTIONAL_STRING_RULE,
    "owner": OPTIONAL_STRING_RULE,
    "tags": STRING_TUPLE_RULE,
    "is_active": BOOLEAN_RULE,
    "notes": OPTIONAL_STRING_RULE,
}