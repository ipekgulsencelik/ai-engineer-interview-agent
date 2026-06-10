from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.interview_report_result_validator import (
    InterviewReportResultValidator,
)


@dataclass(frozen=True)
class InterviewReportResult:
    """
    Final interview intelligence report snapshot.
    """

    candidate_level: str

    overall_score: float

    market_alignment_score: float

    evaluated_questions: int

    strengths: tuple[str, ...]

    weaknesses: tuple[str, ...]

    recommendations: tuple[str, ...]

    category_scores: tuple[
        tuple[str, float],
        ...,
    ]

    def __post_init__(
        self,
    ) -> None:
        InterviewReportResultValidator.validate(
            self,
        )