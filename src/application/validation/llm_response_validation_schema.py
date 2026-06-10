from __future__ import annotations

from typing import Final

from src.application.models.llm_response_metadata import (
    LLMResponseMetadata,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


NON_EMPTY_STRING_RULE: Final[
    ValidationRule
] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}


LLM_RESPONSE_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "text": (
        NON_EMPTY_STRING_RULE
    ),
    "metadata": {
        "type": LLMResponseMetadata,
        "nullable": False,
    },
}