from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.evaluation.evaluator import Evaluator
from src.domain.results.evaluation_result import EvaluationResult
from src.shared.logging.logger import logger


class FallbackEvaluator(Evaluator):
    """
    Tries the primary evaluator; on any failure uses the fallback.

    Keeps an interview going when the LLM provider is down, rate limited or
    returns unparseable output. The fallback result's rubric_version shows
    which evaluator actually graded the answer.
    """

    def __init__(self, *, primary: Evaluator, fallback: Evaluator) -> None:
        self._primary = primary
        self._fallback = fallback

    def evaluate(self, *, question: Question, answer: str) -> EvaluationResult:
        try:
            return self._primary.evaluate(question=question, answer=answer)
        except Exception as exc:  # noqa: BLE001 - any provider failure degrades
            logger.warning(
                "Primary evaluator failed; using fallback.",
                question_id=question.id,
                error_type=type(exc).__name__,
            )
            return self._fallback.evaluate(question=question, answer=answer)
