from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DATASET_SPLIT_SCHEMA: Final[SchemaDefinition] = {
    "sample_ids": STRING_TUPLE_RULE,
}