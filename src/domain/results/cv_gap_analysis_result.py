from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.cv_gap_analysis_result_validator import (
    CVGapAnalysisResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CVGapAnalysisResult:
    """
    Candidate skill gap analysis result model.

    Bu model:
        - candidate skill alignment
        - missing competency detection
        - recommendation generation

    süreçlerinde kullanılan immutable analysis snapshot modelidir.
    """

    matched_skills: tuple[str, ...]

    missing_skills: tuple[str, ...]

    alignment_score: float

    recommended_focus_areas: tuple[str, ...]

    def __post_init__(self) -> None:
        CVGapAnalysisResultValidator.validate(
            self,
        )