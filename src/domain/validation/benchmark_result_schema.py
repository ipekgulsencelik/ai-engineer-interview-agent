from __future__ import annotations

from typing import Final

from src.domain.validation.schema_types import (
    ValidationRule,
)


NUMBER_TYPES: Final[tuple[type[int], type[float]]] = (
    int,
    float,
)

MIN_RETRIEVED_COUNT: Final[int] = 0

MIN_LATENCY_SECONDS: Final[float] = 0.0

MIN_SCORE: Final[float] = 0.0


BENCHMARK_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}


BENCHMARK_OPTIONAL_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": True,
    "non_empty": True,
}


BENCHMARK_RETRIEVED_COUNT_RULE: Final[ValidationRule] = {
    "type": int,
    "nullable": False,
    "reject_bool": True,
    "min_value": MIN_RETRIEVED_COUNT,
}


BENCHMARK_OPTIONAL_SCORE_RULE: Final[ValidationRule] = {
    "type": NUMBER_TYPES,
    "nullable": True,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_SCORE,
}


BENCHMARK_BOOLEAN_RULE: Final[ValidationRule] = {
    "type": bool,
    "nullable": False,
}


BENCHMARK_LATENCY_RULE: Final[ValidationRule] = {
    "type": NUMBER_TYPES,
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_LATENCY_SECONDS,
}