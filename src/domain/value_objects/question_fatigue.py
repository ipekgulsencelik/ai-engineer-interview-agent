from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.question_fatigue_validator import (
    QuestionFatigueValidator,
)


@dataclass(frozen=True, slots=True)
class QuestionFatigue:
    """
    Interview fatigue snapshot.
    """

    repeated_category_count: int
    repeated_question_type_count: int
    recent_high_difficulty_count: int

    def __post_init__(self) -> None:
        QuestionFatigueValidator.validate(self)