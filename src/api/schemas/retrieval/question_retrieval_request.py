from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

from src.api.constants.retrieval import (
    DEFAULT_TOP_K,
    MAX_TOP_K,
    MIN_TOP_K,
)
from src.api.schemas.evaluation.enums import (
    QuestionLevel,
)
from src.api.schemas.evaluation.primitives import (
    NonEmptyString,
)
from src.api.validators.interview_step_request_validator import (
    InterviewStepRequestValidator,
)


class QuestionRetrievalRequest(BaseModel):
    """
    Semantic question retrieval request schema.
    """

    query: NonEmptyString

    current_level: QuestionLevel

    top_k: int = Field(
        default=DEFAULT_TOP_K,
        ge=MIN_TOP_K,
        le=MAX_TOP_K,
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