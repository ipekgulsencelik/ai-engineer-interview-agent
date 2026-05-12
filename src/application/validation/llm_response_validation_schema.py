from __future__ import annotations

from typing import Any

from src.application.models.llm_response_metadata import (
    LLMResponseMetadata,
)


LLM_RESPONSE_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "text": {
        "type": str,
        "non_empty": True,
    },
    "metadata": {
        "type": LLMResponseMetadata,
    },
}