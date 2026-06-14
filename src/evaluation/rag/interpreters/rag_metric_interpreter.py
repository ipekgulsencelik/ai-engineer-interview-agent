from __future__ import annotations

from src.evaluation.rag.constants.rag_interpretation_labels import (
    RAG_EVALUATION_PASSED,
)
from src.evaluation.rag.evaluators.rag_failure_reason_evaluator import (
    RagFailureReasonEvaluator,
)


class RAGMetricInterpreter:
    """
    Produces interpretation labels for RAG evaluation outcomes.
    """

    def __init__(
        self,
        *,
        failure_reason_evaluator: (
            RagFailureReasonEvaluator | None
        ) = None,
    ) -> None:
        self._failure_reason_evaluator = (
            failure_reason_evaluator
            or RagFailureReasonEvaluator()
        )

    def interpret(
        self,
        *,
        retrieval_precision: float,
        retrieval_recall: float,
        context_relevance_score: float,
        faithfulness_score: float,
        answer_relevance_score: float,
        answer_correctness_score: float,
        overall_score: float,
        hallucination_detected: bool,
    ) -> str:
        failure_reason = (
            self._failure_reason_evaluator.evaluate(
                retrieval_precision=(
                    retrieval_precision
                ),
                retrieval_recall=retrieval_recall,
                context_relevance_score=(
                    context_relevance_score
                ),
                faithfulness_score=(
                    faithfulness_score
                ),
                answer_relevance_score=(
                    answer_relevance_score
                ),
                answer_correctness_score=(
                    answer_correctness_score
                ),
                overall_score=overall_score,
                hallucination_detected=(
                    hallucination_detected
                ),
            )
        )

        if failure_reason is None:
            return RAG_EVALUATION_PASSED

        return failure_reason
RagMetricInterpreter = RAGMetricInterpreter
