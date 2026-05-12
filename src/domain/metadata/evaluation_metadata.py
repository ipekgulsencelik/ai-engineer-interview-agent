from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace

from src.domain.constants.evaluation import (
    DEFAULT_CONFIDENCE_SCORE,
    DEFAULT_RUBRIC_VERSION,
)
from src.domain.validators.evaluation_metadata_validator import (
    EvaluationMetadataValidator,
)


@dataclass(frozen=True)
class EvaluationMetadata:
    """
    Provider-independent evaluation execution metadata value object.
    """

    confidence: float = DEFAULT_CONFIDENCE_SCORE
    rubric_version: str = DEFAULT_RUBRIC_VERSION
    latency_seconds: float | None = None
    missing_keywords: tuple[str, ...] = field(
        default_factory=tuple,
    )
    follow_up_question: str | None = None

    def __post_init__(self) -> None:
        EvaluationMetadataValidator.validate(
            self,
        )

    def with_latency_seconds(
        self,
        latency_seconds: float,
    ) -> EvaluationMetadata:
        return replace(
            self,
            latency_seconds=latency_seconds,
        )