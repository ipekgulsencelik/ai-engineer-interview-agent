from __future__ import annotations

from src.evaluation.rag.constants.rag_interpretation_labels import RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION
from src.evaluation.rag.evaluators.rag_failure_reason_evaluator import RAGFailureReasonEvaluator


def test_rag_failure_reason_evaluator_should_return_first_failing_reason() -> None:
    assert RAGFailureReasonEvaluator.evaluate(
        retrieval_precision=0.0,
        retrieval_recall=1.0,
        context_relevance_score=1.0,
        faithfulness_score=1.0,
        answer_relevance_score=1.0,
        answer_correctness_score=1.0,
        overall_score=1.0,
        hallucination_detected=False,
    ) == RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION
