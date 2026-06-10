from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_NEGATIVE_NUMBER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


CONFIDENCE_INTERVAL_SCHEMA: Final[
    SchemaDefinition
] = {
    "lower_bound": NON_NEGATIVE_NUMBER_RULE,
    "upper_bound": NON_NEGATIVE_NUMBER_RULE,
    "confidence_level": NON_NEGATIVE_NUMBER_RULE,
}