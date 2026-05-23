from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict

from src.api.schemas.evaluation.enums import (
    QuestionLevel,
)
from src.api.schemas.evaluation.primitives import (
    NonEmptyString,
    Score,
)


class InterviewStepResponse(BaseModel):
    """
    Adaptive interview orchestration response schema.
    """

    question_id: NonEmptyString

    question_text: NonEmptyString

    score: Score

    feedback: NonEmptyString

    next_level: QuestionLevel

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )