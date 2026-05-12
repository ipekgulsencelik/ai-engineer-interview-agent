from __future__ import annotations

from dataclasses import dataclass, field

from src.application.validators.llm_request_validator import (
    LLMRequestValidator,
)


@dataclass(frozen=True)
class LLMRequest:
    """
    Provider-independent text generation request modelidir.
    """

    prompt: str

    system_prompt: str | None = None

    temperature: float | None = None

    max_tokens: int | None = None

    stop: tuple[str, ...] = field(
        default_factory=tuple,
    )

    def __post_init__(self) -> None:
        LLMRequestValidator.validate(self)