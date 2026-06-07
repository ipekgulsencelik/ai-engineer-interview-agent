from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EVALUATION_DATASET_SCHEMA: Final[SchemaDefinition] = {
    "dataset_id": NON_EMPTY_STRING_RULE,
    "dataset_name": NON_EMPTY_STRING_RULE,
    "description": NON_EMPTY_STRING_RULE,
}