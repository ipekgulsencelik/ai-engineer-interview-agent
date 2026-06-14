from __future__ import annotations

from src.evaluation.rag.constants.rag_interpretation_labels import (
    RAG_FAILED_DUE_TO_HALLUCINATION,
    RAG_FAILED_DUE_TO_LOW_ANSWER_CORRECTNESS,
    RAG_FAILED_DUE_TO_LOW_ANSWER_RELEVANCE,
    RAG_FAILED_DUE_TO_LOW_CONTEXT_RELEVANCE,
    RAG_FAILED_DUE_TO_LOW_FAITHFULNESS,
    RAG_FAILED_DUE_TO_LOW_OVERALL_SCORE,
    RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION,
    RAG_FAILED_DUE_TO_LOW_RETRIEVAL_RECALL,
)
from src.evaluation.rag.constants.rag_thresholds import (
    MINIMUM_ANSWER_CORRECTNESS_SCORE,
    MINIMUM_ANSWER_RELEVANCE_SCORE,
    MINIMUM_CONTEXT_RELEVANCE_SCORE,
    MINIMUM_FAITHFULNESS_SCORE,
    MINIMUM_OVERALL_RAG_SCORE,
    MINIMUM_RETRIEVAL_PRECISION,
    MINIMUM_RETRIEVAL_RECALL,
)


class RAGFailureReasonEvaluator:
    """
    Evaluates the first failing RAG quality reason.
    """

    @staticmethod
    def evaluate(
        *,
        retrieval_precision: float,
        retrieval_recall: float,
        context_relevance_score: float,
        faithfulness_score: float,
        answer_relevance_score: float,
        answer_correctness_score: float,
        overall_score: float,
        hallucination_detected: bool,
    ) -> str | None:
        if hallucination_detected:
            return RAG_FAILED_DUE_TO_HALLUCINATION

        if (
            retrieval_precision
            < MINIMUM_RETRIEVAL_PRECISION
        ):
            return (
                RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION
            )

        if (
            retrieval_recall
            < MINIMUM_RETRIEVAL_RECALL
        ):
            return (
                RAG_FAILED_DUE_TO_LOW_RETRIEVAL_RECALL
            )

        if (
            context_relevance_score
            < MINIMUM_CONTEXT_RELEVANCE_SCORE
        ):
            return (
                RAG_FAILED_DUE_TO_LOW_CONTEXT_RELEVANCE
            )

        if (
            faithfulness_score
            < MINIMUM_FAITHFULNESS_SCORE
        ):
            return RAG_FAILED_DUE_TO_LOW_FAITHFULNESS

        if (
            answer_relevance_score
            < MINIMUM_ANSWER_RELEVANCE_SCORE
        ):
            return (
                RAG_FAILED_DUE_TO_LOW_ANSWER_RELEVANCE
            )

        if (
            answer_correctness_score
            < MINIMUM_ANSWER_CORRECTNESS_SCORE
        ):
            return (
                RAG_FAILED_DUE_TO_LOW_ANSWER_CORRECTNESS
            )

        if overall_score < MINIMUM_OVERALL_RAG_SCORE:
            return RAG_FAILED_DUE_TO_LOW_OVERALL_SCORE

        return None
RagFailureReasonEvaluator = RAGFailureReasonEvaluator
