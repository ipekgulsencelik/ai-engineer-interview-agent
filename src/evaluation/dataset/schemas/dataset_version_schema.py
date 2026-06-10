from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    SEMVER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DATASET_VERSION_SCHEMA: Final[SchemaDefinition] = {
    "version": SEMVER_RULE,
    "created_by": NON_EMPTY_STRING_RULE,
    "description": NON_EMPTY_STRING_RULE,
}