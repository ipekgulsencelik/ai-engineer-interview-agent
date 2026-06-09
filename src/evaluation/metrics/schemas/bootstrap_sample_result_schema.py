from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_NEGATIVE_INTEGER_RULE,
    NUMBER_RULE,
    OPTIONAL_INTEGER_RULE,
    POSITIVE_INTEGER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BOOTSTRAP_SAMPLE_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "sample_index": NON_NEGATIVE_INTEGER_RULE,
    "sample_size": POSITIVE_INTEGER_RULE,
    "statistic_value": NUMBER_RULE,
    "seed": OPTIONAL_INTEGER_RULE,
}