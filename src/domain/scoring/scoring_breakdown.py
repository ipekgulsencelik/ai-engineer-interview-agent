from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.selection_breakdown_validator import (
    SelectionBreakdownValidator,
)

@dataclass(frozen=True)
class ScoringBreakdown:
    """
    Explainable scoring breakdown modelidir.
    """

    level_score: float
    market_score: float
    cv_gap_score: float
    difficulty_score: float
    diversity_score: float
    fatigue_score: float
    final_score: float

    def __post_init__(self) -> None:
        ScoringBreakdownValidator.validate(self)