from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    CORRELATION_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    P_VALUE_RULE,
    POSITIVE_INTEGER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


CORRELATION_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "metric_x": NON_EMPTY_STRING_RULE,
    "metric_y": NON_EMPTY_STRING_RULE,
    "correlation_coefficient": CORRELATION_RULE,
    "p_value": P_VALUE_RULE,
    "sample_count": POSITIVE_INTEGER_RULE,
    "method": NON_EMPTY_STRING_RULE,
    "is_significant": BOOLEAN_RULE,
    "notes": OPTIONAL_STRING_RULE,
}