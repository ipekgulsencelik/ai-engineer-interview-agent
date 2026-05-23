from __future__ import annotations

from typing import Final

from src.application.constants.llm import (
    MAX_LLM_TEMPERATURE,
    MIN_LLM_TEMPERATURE,
    MIN_MAX_TOKENS,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


REQUIRED_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}

OPTIONAL_STRING_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": True,
    "non_empty": True,
}

TEMPERATURE_RULE: Final[ValidationRule] = {
    "type": (int, float),
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_LLM_TEMPERATURE,
    "max_value": MAX_LLM_TEMPERATURE,
}

MAX_TOKENS_RULE: Final[ValidationRule] = {
    "type": int,
    "nullable": False,
    "reject_bool": True,
    "min_value": MIN_MAX_TOKENS,
}

STOP_RULE: Final[ValidationRule] = {
    "type": tuple,
    "nullable": False,
    "item_type": str,
    "non_empty_items": True,
}


LLM_REQUEST_VALIDATION_SCHEMA: Final[ValidationSchema] = {
    "prompt": REQUIRED_STRING_RULE,
    "system_prompt": OPTIONAL_STRING_RULE,
    "temperature": TEMPERATURE_RULE,
    "max_tokens": MAX_TOKENS_RULE,
    "stop": STOP_RULE,
}