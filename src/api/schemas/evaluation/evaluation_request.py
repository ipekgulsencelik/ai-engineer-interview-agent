from __future__ import annotations

from typing import Annotated
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

from src.api.constants.evaluation import (
    DEFAULT_MARKET_WEIGHT,
    MAX_DIFFICULTY,
    MIN_DIFFICULTY,
)
from src.api.schemas.evaluation.enums import (
    QuestionLevel,
    QuestionType,
)
from src.api.schemas.evaluation.primitives import (
    NonEmptyString,
    PositiveFloat,
)
from src.api.validators.evaluation_request_validator import (
    EvaluationRequestValidator,
)


class EvaluationRequest(BaseModel):
    """
    Candidate answer evaluation request schema.
    """

    question_id: NonEmptyString

    question_text: NonEmptyString

    category: NonEmptyString

    level: QuestionLevel

    difficulty: Annotated[
        int,
        Field(
            ge=MIN_DIFFICULTY,
            le=MAX_DIFFICULTY,
        ),
    ]

    question_type: QuestionType

    expected_points: list[NonEmptyString] = Field(
        default_factory=list,
    )

    keywords: list[NonEmptyString] = Field(
        default_factory=list,
    )

    market_weight: PositiveFloat = (
        DEFAULT_MARKET_WEIGHT
    )

    answer: NonEmptyString

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    @field_validator(
        "level",
        mode="before",
    )
    @classmethod
    def normalize_level(
        cls,
        value: Any,
    ) -> Any:
        return (
            EvaluationRequestValidator
            .normalize_level(
                value,
            )
        )

    @field_validator(
        "difficulty",
        mode="before",
    )
    @classmethod
    def normalize_difficulty(
        cls,
        value: Any,
    ) -> Any:
        return (
            EvaluationRequestValidator
            .normalize_difficulty(
                value,
            )
        )

    @field_validator(
        "question_type",
        mode="before",
    )
    @classmethod
    def normalize_question_type(
        cls,
        value: Any,
    ) -> Any:
        return (
            EvaluationRequestValidator
            .normalize_question_type(
                value,
            )
        )