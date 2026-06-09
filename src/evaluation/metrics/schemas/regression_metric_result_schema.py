from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    POSITIVE_INTEGER_RULE,
    R2_SCORE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


REGRESSION_METRIC_RESULT_SCHEMA: Final[SchemaDefinition] = {
    "metric_name": NON_EMPTY_STRING_RULE,
    "mae": NON_NEGATIVE_NUMBER_RULE,
    "mse": NON_NEGATIVE_NUMBER_RULE,
    "rmse": NON_NEGATIVE_NUMBER_RULE,
    "r2_score": R2_SCORE_RULE,
    "sample_count": POSITIVE_INTEGER_RULE,
    "is_acceptable": BOOLEAN_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}