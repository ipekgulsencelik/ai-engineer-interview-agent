from __future__ import annotations

from src.domain.constants.diversity_scoring import (
    DEFAULT_DIVERSITY_SCORE,
)
from src.domain.entities.question import Question
from src.domain.scoring.normalized_score_clamper import (
    NormalizedScoreClamper,
)
from src.domain.scoring.repeat_penalty_policy import (
    RepeatPenaltyPolicy,
)
from src.domain.value_objects.interview_coverage import (
    InterviewCoverage,
)


class DiversityScoreCalculator:
    """
    Interview diversity scoring policy.

    Amaç:
        - category repetition azaltmak
        - question type repetition azaltmak
        - balanced interview coverage sağlamak
    """

    @classmethod
    def calculate(
        cls,
        *,
        question: Question,
        coverage: InterviewCoverage,
    ) -> float:
        if coverage.total_questions == 0:
            return DEFAULT_DIVERSITY_SCORE

        category_repeat_count = (
            coverage.category_counts.get(
                question.category.value,
                0,
            )
        )

        question_type_repeat_count = (
            coverage.question_type_counts.get(
                question.question_type.value,
                0,
            )
        )

        category_penalty = (
            RepeatPenaltyPolicy.calculate(
                repeat_count=category_repeat_count,
            )
        )

        type_penalty = (
            RepeatPenaltyPolicy.calculate(
                repeat_count=question_type_repeat_count,
            )
        )

        diversity_score = (
            DEFAULT_DIVERSITY_SCORE
            - category_penalty
            - type_penalty
        )

        return NormalizedScoreClamper.clamp(
            score=diversity_score,
        )