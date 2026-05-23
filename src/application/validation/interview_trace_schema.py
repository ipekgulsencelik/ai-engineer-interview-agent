from __future__ import annotations

from typing import Final

from src.domain.validation.schema_types import (
    ValidationRule,
)


NON_EMPTY_TRACE_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}

NON_NEGATIVE_INTEGER_RULE: Final[ValidationRule] = {
    "type": int,
    "nullable": False,
    "reject_bool": True,
    "min_value": 0,
}

NON_NEGATIVE_LATENCY_RULE: Final[ValidationRule] = {
    "type": (int, float),
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": 0.0,
}