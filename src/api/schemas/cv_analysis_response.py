from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from src.api.schemas.evaluation.enums import (
    QuestionLevel,
)
from src.api.schemas.evaluation.primitives import (
    NonEmptyString,
    PositiveFloat,
    Score,
)


class CVAnalysisResponse(BaseModel):
    """
    Candidate CV analysis response schema.
    """

    detected_level: QuestionLevel

    years_of_experience: PositiveFloat

    skills: list[NonEmptyString] = Field(
        default_factory=list,
    )

    weak_skills: list[NonEmptyString] = Field(
        default_factory=list,
    )

    matched_skills: list[NonEmptyString] = Field(
        default_factory=list,
    )

    missing_skills: list[NonEmptyString] = Field(
        default_factory=list,
    )

    alignment_score: Score

    recommended_focus_areas: list[
        NonEmptyString
    ] = Field(
        default_factory=list,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )