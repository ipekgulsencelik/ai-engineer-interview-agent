from __future__ import annotations

from src.api.constants.response import (
    FINAL_SCORE_PRECISION,
)
from src.api.schemas.evaluation.enums import (
    QuestionLevel,
)
from src.api.schemas.interview.responses import (
    InterviewQuestionResponse,
)
from src.domain.results.selection_result import (
    SelectionResult,
)


class InterviewQuestionResponseMapper:
    """
    SelectionResult -> InterviewQuestionResponse mapper.
    """

    @staticmethod
    def from_selection_result(
        *,
        result: SelectionResult,
    ) -> InterviewQuestionResponse:
        question = result.question

        return InterviewQuestionResponse(
            id=question.id,
            text=question.text,
            category=question.category.value,
            level=QuestionLevel(question.level.value),
            question_type=(
                question.question_type.value
            ),
            difficulty=question.difficulty,
            final_score=round(
                result.breakdown.final_score,
                FINAL_SCORE_PRECISION,
            ),
        )