from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NUMBER_RULE,
    OPTIONAL_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_INTEGER_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


SIGNIFICANCE_TEST_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "test_name": NON_EMPTY_STRING_RULE,
    "statistic": NUMBER_RULE,
    "p_value": RATIO_RULE,
    "alpha": RATIO_RULE,
    "is_significant": BOOLEAN_RULE,
    "sample_count": POSITIVE_INTEGER_RULE,
    "effect_size": OPTIONAL_NUMBER_RULE,
    "interpretation": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}