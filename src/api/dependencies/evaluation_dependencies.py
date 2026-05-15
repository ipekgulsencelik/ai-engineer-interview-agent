from __future__ import annotations

from src.application.services.answer_evaluation_service import (
    AnswerEvaluationService,
)


def get_answer_evaluation_service() -> AnswerEvaluationService:
    """
    AnswerEvaluationService dependency provider.

    Not:
        Şimdilik doğrudan instance üretiyoruz.
        Sonraki adımda burada evaluator, LLM client ve parser wiring yapılacak.
    """

    return AnswerEvaluationService()