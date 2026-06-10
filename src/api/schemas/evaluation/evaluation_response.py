from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from src.api.constants.evaluation import (
    MIN_LATENCY_SECONDS,
)
from src.api.schemas.evaluation.primitives import (
    NonEmptyString,
    Score,
)


class EvaluationResponse(BaseModel):
    """
    Candidate evaluation response schema.
    """

    score: Score

    feedback: NonEmptyString

    technical_accuracy: Score

    depth: Score

    communication: Score

    confidence: Score

    missing_keywords: list[NonEmptyString] = Field(
        default_factory=list,
    )

    follow_up_question: str | None = None

    latency_seconds: float | None = Field(
        default=None,
        ge=MIN_LATENCY_SECONDS,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )