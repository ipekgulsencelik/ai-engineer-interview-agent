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


class InterviewQuestionResponse(BaseModel):
    """
    Semantic interview question retrieval response schema.
    """

    id: NonEmptyString

    text: NonEmptyString

    category: NonEmptyString

    level: QuestionLevel

    question_type: NonEmptyString

    difficulty: int

    final_score: Score

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )