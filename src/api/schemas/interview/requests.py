from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

from src.api.schemas.evaluation.enums import (
    QuestionLevel,
)
from src.api.schemas.evaluation.primitives import (
    NonEmptyString,
    Score,
)
from src.api.validators.interview_step_request_validator import (
    InterviewStepRequestValidator,
)


class InterviewStepRequest(BaseModel):
    """
    Adaptive interview orchestration request schema.
    """

    query: NonEmptyString

    answer: NonEmptyString

    current_level: QuestionLevel

    cv_skills: list[NonEmptyString] = Field(
        default_factory=list,
    )

    recent_scores: list[Score] = Field(
        default_factory=list,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    @field_validator(
        "current_level",
        mode="before",
    )
    @classmethod
    def normalize_current_level(
        cls,
        value: object,
    ) -> object:
        return (
            InterviewStepRequestValidator
            .normalize_current_level(value)
        )