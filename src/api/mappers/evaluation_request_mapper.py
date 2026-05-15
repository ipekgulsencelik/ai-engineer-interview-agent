from __future__ import annotations

from src.api.schemas.evaluation.requests import EvaluationRequest
from src.domain.entities.question import Question


class EvaluationRequestMapper:
    """
    EvaluationRequest API schema'sını domain Question entity'sine dönüştürür.

    Bu sınıf:
        - API contract ile domain model arasındaki mapping sorumluluğunu taşır
        - route içinde domain entity oluşturma karmaşasını engeller
        - API layer ile domain layer arasındaki translation boundary'dir
    """

    @staticmethod
    def to_question(
        request: EvaluationRequest,
    ) -> Question:
        """
        EvaluationRequest içindeki question alanlarından Question entity üretir.
        """

        return Question(
            id=request.question_id,
            text=request.question_text,
            category=request.category,
            level=request.level.value,
            difficulty=request.difficulty,
            question_type=request.question_type.value,
            expected_points=tuple(request.expected_points),
            keywords=tuple(request.keywords),
            market_weight=request.market_weight,
        )