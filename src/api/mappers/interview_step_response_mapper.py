from __future__ import annotations

from src.api.constants.response import (
    FINAL_SCORE_PRECISION,
)
from src.api.schemas.evaluation.enums import (
    QuestionLevel,
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
            next_level=QuestionLevel(next_level.value),
        )

    @staticmethod
    def from_result(
        *,
        result: object,
    ) -> InterviewStepResponse:
        return InterviewStepResponseMapper.from_evaluation_result(
            result=result.evaluation_result,
            next_level=result.next_level,
            question_id=result.selection_result.question.id,
            question_text=result.selection_result.question.text,
        )