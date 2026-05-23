from __future__ import annotations

from datetime import datetime
from typing import Final

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.constants.selection import (
    MAX_NORMALIZED_SCORE,
    MIN_FINAL_SCORE,
    MIN_NORMALIZED_SCORE,
)
from src.domain.validation.schema_types import (
    ValidationRule,
)


NUMBER_TYPES: Final[tuple[type, type]] = (
    int,
    float,
)


NON_EMPTY_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
    "strip": True,
}


OPTIONAL_NON_EMPTY_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": True,
    "non_empty": True,
    "strip": True,
}


BOOLEAN_RULE: Final[ValidationRule] = {
    "type": bool,
    "nullable": False,
}


FINITE_NUMBER_RULE: Final[ValidationRule] = {
    "type": NUMBER_TYPES,
    "reject_bool": True,
    "finite": True,
    "nullable": False,
}


NON_NEGATIVE_NUMBER_RULE: Final[ValidationRule] = {
    **FINITE_NUMBER_RULE,
    "min_value": 0.0,
}


EVALUATION_SCORE_RULE: Final[ValidationRule] = {
    **FINITE_NUMBER_RULE,
    "min_value": MIN_EVALUATION_SCORE,
    "max_value": MAX_EVALUATION_SCORE,
}


NORMALIZED_SCORE_RULE: Final[ValidationRule] = {
    **FINITE_NUMBER_RULE,
    "min_value": MIN_NORMALIZED_SCORE,
    "max_value": MAX_NORMALIZED_SCORE,
}


FINAL_SCORE_RULE: Final[ValidationRule] = {
    **FINITE_NUMBER_RULE,
    "min_value": MIN_FINAL_SCORE,
}


STRING_LIST_RULE: Final[ValidationRule] = {
    "type": list,
    "item_type": str,
    "nullable": False,
}


STRING_TUPLE_RULE: Final[ValidationRule] = {
    "type": tuple,
    "item_type": str,
    "nullable": False,
}


STRING_FROZENSET_RULE: Final[ValidationRule] = {
    "type": frozenset,
    "item_type": str,
    "nullable": False,
}


EVALUATION_SCORE_TUPLE_RULE: Final[ValidationRule] = {
    "type": tuple,
    "item_type": NUMBER_TYPES,
    "reject_bool_items": True,
    "finite_items": True,
    "min_item_value": MIN_EVALUATION_SCORE,
    "max_item_value": MAX_EVALUATION_SCORE,
    "nullable": False,
}


UTC_DATETIME_RULE: Final[ValidationRule] = {
    "type": datetime,
    "timezone_aware": True,
    "nullable": False,
}