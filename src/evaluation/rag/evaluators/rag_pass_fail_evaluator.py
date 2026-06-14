from __future__ import annotations

from src.evaluation.rag.constants.rag_thresholds import (
    MINIMUM_ANSWER_CORRECTNESS_SCORE,
    MINIMUM_ANSWER_RELEVANCE_SCORE,
    MINIMUM_CONTEXT_RELEVANCE_SCORE,
    MINIMUM_FAITHFULNESS_SCORE,
    MINIMUM_OVERALL_RAG_SCORE,
    MINIMUM_RETRIEVAL_PRECISION,
    MINIMUM_RETRIEVAL_RECALL,
)


class RagPassFailEvaluator:
    """
    Evaluates whether a RAG evaluation passes
    configured quality thresholds.
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
    ) -> bool:
        if hallucination_detected:
            return False

        return (
            retrieval_precision
            >= MINIMUM_RETRIEVAL_PRECISION
            and retrieval_recall
            >= MINIMUM_RETRIEVAL_RECALL
            and context_relevance_score
            >= MINIMUM_CONTEXT_RELEVANCE_SCORE
            and faithfulness_score
            >= MINIMUM_FAITHFULNESS_SCORE
            and answer_relevance_score
            >= MINIMUM_ANSWER_RELEVANCE_SCORE
            and answer_correctness_score
            >= MINIMUM_ANSWER_CORRECTNESS_SCORE
            and overall_score
            >= MINIMUM_OVERALL_RAG_SCORE
        )