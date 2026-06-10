from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    CORRELATION_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    P_VALUE_RULE,
    POSITIVE_INTEGER_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


AGREEMENT_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "metric_name": NON_EMPTY_STRING_RULE,
    "kappa_score": CORRELATION_RULE,
    "agreement_ratio": RATIO_RULE,
    "sample_count": POSITIVE_INTEGER_RULE,
    "evaluator_count": POSITIVE_INTEGER_RULE,
    "method": NON_EMPTY_STRING_RULE,
    "is_reliable": BOOLEAN_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "p_value": P_VALUE_RULE,
    "notes": OPTIONAL_STRING_RULE,
}