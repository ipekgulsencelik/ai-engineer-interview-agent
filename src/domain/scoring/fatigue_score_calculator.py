from __future__ import annotations

from src.domain.constants.fatigue_scoring import (
    DEFAULT_FATIGUE_SCORE,
)
from src.domain.entities.question import Question
from src.domain.scoring.fatigue_penalty_policy import (
    FatiguePenaltyPolicy,
)
from src.domain.scoring.normalized_score_clamper import (
    NormalizedScoreClamper,
)
from src.domain.value_objects.question_fatigue import (
    QuestionFatigue,
)


class FatigueScoreCalculator:
    """
    Interview fatigue score calculation policy.
    """

    @staticmethod
    def calculate(
        *,
        question: Question,
        fatigue: QuestionFatigue,
    ) -> float:
        penalty = FatiguePenaltyPolicy.calculate(
            question=question,
            fatigue=fatigue,
        )

        score = DEFAULT_FATIGUE_SCORE - penalty

        return NormalizedScoreClamper.clamp(
            score=score,
        )