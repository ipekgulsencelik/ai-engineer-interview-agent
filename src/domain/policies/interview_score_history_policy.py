from __future__ import annotations

from src.domain.constants.interview_session import (
    MAX_RECENT_SCORES_HISTORY,
)


class InterviewScoreHistoryPolicy:
    """
    Interview score history update policy.
    """

    @staticmethod
    def append_score(
        *,
        recent_scores: tuple[float, ...],
        evaluation_score: float,
    ) -> tuple[float, ...]:
        updated_scores = (
            recent_scores
            + (evaluation_score,)
        )

        return updated_scores[
            -MAX_RECENT_SCORES_HISTORY:
        ]