from __future__ import annotations

from dataclasses import dataclass, field

from src.application.models.llm_response_metadata import (
    LLMResponseMetadata,
)
from src.application.validators.llm_response_validator import (
    LLMResponseValidator,
)


@dataclass(frozen=True, slots=True)
class LLMResponse:
    """
    Provider-independent normalized text generation response model.

    Bu model:
        - raw SDK response değildir
        - provider-independent response abstraction sağlar
        - evaluator/parser pipeline için standart input oluşturur
        - generation text ve runtime metadata taşır
    """

    text: str

    metadata: LLMResponseMetadata = field(
        default_factory=LLMResponseMetadata,
    )

    def __post_init__(self) -> None:
        LLMResponseValidator.validate(self)