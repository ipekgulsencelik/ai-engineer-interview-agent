from __future__ import annotations

from typing import Final

from src.application.constants.llm_metadata import (
    MIN_LATENCY_SECONDS,
    MIN_TOKEN_COUNT,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


NON_EMPTY_OPTIONAL_STRING_RULE: Final[
    ValidationRule
] = {
    "type": str,
    "nullable": True,
    "non_empty": True,
}


NON_NEGATIVE_INT_RULE: Final[
    ValidationRule
] = {
    "type": int,
    "nullable": True,
    "reject_bool": True,
    "min_value": MIN_TOKEN_COUNT,
}


NON_NEGATIVE_FLOAT_RULE: Final[
    ValidationRule
] = {
    "type": (int, float),
    "nullable": True,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_LATENCY_SECONDS,
}


LLM_RESPONSE_METADATA_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "model_name": (
        NON_EMPTY_OPTIONAL_STRING_RULE
    ),
    "provider_name": (
        NON_EMPTY_OPTIONAL_STRING_RULE
    ),
    "prompt_tokens": (
        NON_NEGATIVE_INT_RULE
    ),
    "completion_tokens": (
        NON_NEGATIVE_INT_RULE
    ),
    "total_tokens": (
        NON_NEGATIVE_INT_RULE
    ),
    "latency_seconds": (
        NON_NEGATIVE_FLOAT_RULE
    ),
    "finish_reason": (
        NON_EMPTY_OPTIONAL_STRING_RULE
    ),
    "raw_response": {
        "type": dict,
        "nullable": True,
    },
}