from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_INTEGER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BOOTSTRAP_DISTRIBUTION_SUMMARY_SCHEMA: Final[SchemaDefinition] = {
    "metric_name": NON_EMPTY_STRING_RULE,
    "bootstrap_iterations": POSITIVE_INTEGER_RULE,
    "mean_score": NON_NEGATIVE_NUMBER_RULE,
    "std_deviation": NON_NEGATIVE_NUMBER_RULE,
    "min_score": NON_NEGATIVE_NUMBER_RULE,
    "max_score": NON_NEGATIVE_NUMBER_RULE,
    "notes": OPTIONAL_STRING_RULE,
}