from __future__ import annotations

from typing import Final

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


NUMBER_TYPES: Final[tuple[type[int], type[float]]] = (
    int,
    float,
)

MIN_LATENCY_SECONDS: Final[float] = 0.0


EVALUATION_RESPONSE_SCORE_RULE: Final[ValidationRule] = {
    "type": NUMBER_TYPES,
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_EVALUATION_SCORE,
    "max_value": MAX_EVALUATION_SCORE,
}


EVALUATION_RESPONSE_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}


EVALUATION_RESPONSE_OPTIONAL_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": True,
    "non_empty": True,
}


EVALUATION_RESPONSE_LATENCY_RULE: Final[ValidationRule] = {
    "type": NUMBER_TYPES,
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_LATENCY_SECONDS,
}


EVALUATION_RESPONSE_STRING_TUPLE_RULE: Final[ValidationRule] = {
    "type": tuple,
    "nullable": False,
    "item_type": str,
    "non_empty_items": True,
}