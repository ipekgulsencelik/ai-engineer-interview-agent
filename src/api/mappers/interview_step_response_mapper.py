from __future__ import annotations

from src.api.constants.response import (
    FINAL_SCORE_PRECISION,
)
from src.api.schemas.interview.responses import (
    InterviewStepResponse,
)
from src.domain.enums.level import (
    Level,
)
from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class InterviewStepResponseMapper:
    """
    EvaluationResult -> InterviewStepResponse mapper.
    """

    @staticmethod
    def from_evaluation_result(
        *,
        result: EvaluationResult,
        next_level: Level,
        question_id: str,
        question_text: str,
    ) -> InterviewStepResponse:
        return InterviewStepResponse(
            question_id=question_id,
            question_text=question_text,
            score=round(
                result.score,
                FINAL_SCORE_PRECISION,
            ),
            feedback=result.feedback,
            next_level=next_level,
        )