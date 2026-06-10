from __future__ import annotations

from typing import Final

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


NON_EMPTY_EVALUATION_TRACE_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}


NON_NEGATIVE_TOKENS_USED_RULE: Final[ValidationRule] = {
    "type": int,
    "nullable": False,
    "reject_bool": True,
    "min_value": 0,
}


NON_NEGATIVE_EVALUATION_LATENCY_RULE: Final[ValidationRule] = {
    "type": (int, float),
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": 0.0,
}


EVALUATION_TRACE_SCORE_RULE: Final[ValidationRule] = {
    "type": (int, float),
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_EVALUATION_SCORE,
    "max_value": MAX_EVALUATION_SCORE,
}