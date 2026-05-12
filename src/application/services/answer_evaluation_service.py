from __future__ import annotations

import time

from src.application.exceptions.answer_evaluation_error import (
    AnswerEvaluationError,
)
from src.domain.evaluation.evaluator import Evaluator
from src.application.validators.answer_evaluation_service_validator import (
    AnswerEvaluationServiceValidator,
)
from src.domain.entities.question import Question
from src.domain.results.evaluation_result import EvaluationResult


class AnswerEvaluationService:
    """
    Candidate answer evaluation use-case orchestration service.
    """

    def __init__(
        self,
        evaluator: Evaluator,
    ) -> None:
        AnswerEvaluationServiceValidator.validate_evaluator(
            evaluator,
        )

        self._evaluator = evaluator

    def evaluate(
        self,
        *,
        question: Question,
        answer: str,
    ) -> EvaluationResult:
        normalized_answer = (
            AnswerEvaluationServiceValidator.validate_evaluation_input(
                question=question,
                answer=answer,
            )
        )

        started_at = time.perf_counter()

        try:
            result = self._evaluator.evaluate(
                question=question,
                answer=normalized_answer,
            )

        except Exception as exc:
            raise AnswerEvaluationError(
                f"Failed to evaluate answer for question "
                f"'{question.id}'."
            ) from exc

        elapsed_seconds = (
            time.perf_counter() - started_at
        )

        AnswerEvaluationServiceValidator.validate_result(
            result,
        )

        return result.with_latency_seconds(
            elapsed_seconds,
        )
