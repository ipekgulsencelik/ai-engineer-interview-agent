from __future__ import annotations

from dataclasses import dataclass, field

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
    Provider-independent evaluation execution metadata modelidir.
    """

    confidence: float = DEFAULT_CONFIDENCE_SCORE
    rubric_version: str = DEFAULT_RUBRIC_VERSION
    latency_seconds: float | None = None
    missing_keywords: tuple[str, ...] = field(default_factory=tuple)
    follow_up_question: str | None = None

    def __post_init__(self) -> None:
        EvaluationMetadataValidator.validate(self)

        