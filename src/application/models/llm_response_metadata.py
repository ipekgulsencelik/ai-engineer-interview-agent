from __future__ import annotations

from dataclasses import dataclass, field

from src.application.validators.llm_response_metadata_validator import (
    LLMResponseMetadataValidator,
)


@dataclass(frozen=True)
class LLMResponseMetadata:
    """
    Provider-independent LLM response metadata modelidir.
    """

    model: str | None = None

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None

    latency_seconds: float | None = None

    finish_reason: str | None = None

    raw_response: dict | None = field(
        default=None,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        LLMResponseMetadataValidator.validate(self)