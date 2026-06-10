from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.interview_coverage_validator import (
    InterviewCoverageValidator,
)


@dataclass(frozen=True, slots=True)
class InterviewCoverage:
    """
    Interview coverage snapshot.
    """

    category_counts: dict[str, int]
    level_counts: dict[str, int]
    question_type_counts: dict[str, int]
    total_questions: int

    def __post_init__(self) -> None:
        InterviewCoverageValidator.validate(self)