from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    SEMVER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


DATASET_METADATA_SCHEMA: Final[SchemaDefinition] = {
    "rubric_version": SEMVER_RULE,
    "evaluator_version": SEMVER_RULE,
    "source": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}