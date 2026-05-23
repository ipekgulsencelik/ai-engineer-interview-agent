from __future__ import annotations

from dataclasses import dataclass

from src.ui.validators.evaluation_response_validator import (
    EvaluationResponseValidator,
)


@dataclass(frozen=True)
class EvaluationResponse:
    """
    Frontend evaluation response model.
    """

    score: float

    technical_accuracy: float

    depth: float

    communication: float

    feedback: str

    follow_up_question: str | None

    confidence: float

    latency_seconds: float

    missing_keywords: tuple[
        str,
        ...,
    ]

    def __post_init__(
        self,
    ) -> None:
        EvaluationResponseValidator.validate(
            self,
        )