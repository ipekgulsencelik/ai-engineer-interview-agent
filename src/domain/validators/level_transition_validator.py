import math

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.constants.level_transition import (
    RECENT_SCORES_MUST_BE_FINITE_ERROR,
    RECENT_SCORES_MUST_BE_LIST_ERROR,
    RECENT_SCORES_MUST_CONTAIN_NUMBERS_ERROR,
    RECENT_SCORES_RANGE_ERROR,
)


class LevelTransitionValidator:
    """Validation rules for level transition input data."""

    @staticmethod
    def validate_recent_scores(
        scores: list[float],
    ) -> None:
        if not isinstance(scores, list):
            raise TypeError(
                RECENT_SCORES_MUST_BE_LIST_ERROR,
            )

        for score in scores:
            if isinstance(score, bool) or not isinstance(score, (int, float)):
                raise TypeError(RECENT_SCORES_MUST_CONTAIN_NUMBERS_ERROR)

            if not math.isfinite(float(score)):
                raise ValueError(RECENT_SCORES_MUST_BE_FINITE_ERROR)

            if (score < MIN_EVALUATION_SCORE) or (score > MAX_EVALUATION_SCORE):
                raise ValueError(RECENT_SCORES_RANGE_ERROR)