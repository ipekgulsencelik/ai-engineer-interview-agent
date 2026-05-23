from __future__ import annotations

from dataclasses import dataclass

from src.ui.validators.question_response_validator import (
    QuestionResponseValidator,
)


@dataclass(frozen=True)
class QuestionResponse:
    """
    Frontend interview question response model.
    """

    id: str

    text: str

    category: str

    level: str

    question_type: str

    difficulty: int

    final_score: float

    def __post_init__(
        self,
    ) -> None:
        QuestionResponseValidator.validate(
            self,
        )