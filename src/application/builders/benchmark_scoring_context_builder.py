from __future__ import annotations

from src.domain.enums.level import (
    Level,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class BenchmarkScoringContextBuilder:
    """
    Benchmark retrieval scoring context builder.
    """

    @staticmethod
    def build() -> ScoringContext:
        return ScoringContext(
            current_level=Level.MID,
            cv_skills=[],
            asked_question_ids=[],
            recent_scores=[],
            weak_areas=[],
        )