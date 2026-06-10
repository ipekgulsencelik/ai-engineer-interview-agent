from __future__ import annotations

from dataclasses import dataclass, field

from src.application.constants.llm import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
)
from src.application.validators.llm_request_validator import (
    LLMRequestValidator,
)


@dataclass(frozen=True, slots=True)
class LLMRequest:
    """
    Provider-independent text generation request model.

    Bu model:
        - provider-independent generation config taşır
        - raw SDK request değildir
        - application layer generation contract'ıdır
        - prompt/config/runtime generation ayarlarını normalize eder
    """

    prompt: str

    system_prompt: str | None = None

    temperature: float = (
        DEFAULT_TEMPERATURE
    )

    max_tokens: int = (
        DEFAULT_MAX_TOKENS
    )

    stop: tuple[str, ...] = field(
        default_factory=tuple,
    )

    def __post_init__(self) -> None:
        LLMRequestValidator.validate(self)