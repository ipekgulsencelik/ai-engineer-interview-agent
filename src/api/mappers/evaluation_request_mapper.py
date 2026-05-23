from __future__ import annotations

from src.api.schemas.evaluation.requests import (
    EvaluationRequest,
)
from src.domain.entities.question import (
    Question,
)
from src.domain.enums.level import (
    Level,
)
from src.domain.enums.question_type import (
    QuestionType,
)


class EvaluationRequestMapper:
    """
    EvaluationRequest -> Question mapper.
    """

    @staticmethod
    def to_question(
        *,
        request: EvaluationRequest,
    ) -> Question:
        return Question(
            id=request.question_id,
            text=request.question_text,
            category=request.category,
            level=Level(
                request.level.value,
            ),
            difficulty=request.difficulty,
            question_type=QuestionType(
                request.question_type.value,
            ),
            expected_points=tuple(
                request.expected_points,
            ),
            keywords=tuple(
                request.keywords,
            ),
            market_weight=request.market_weight,
        )