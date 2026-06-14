from __future__ import annotations

from src.evaluation.rag.constants.rag_interpretation_labels import RAG_EVALUATION_PASSED, RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION
from src.evaluation.rag.interpreters.rag_metric_interpreter import RAGMetricInterpreter


def test_rag_metric_interpreter_should_return_passed_label_when_metrics_pass() -> None:
    assert RAGMetricInterpreter().interpret(
        retrieval_precision=1.0,
        retrieval_recall=1.0,
        context_relevance_score=1.0,
        faithfulness_score=1.0,
        answer_relevance_score=1.0,
        answer_correctness_score=1.0,
        overall_score=1.0,
        hallucination_detected=False,
    ) == RAG_EVALUATION_PASSED


def test_rag_metric_interpreter_should_return_failure_reason_when_metric_fails() -> None:
    assert RAGMetricInterpreter().interpret(
        retrieval_precision=0.0,
        retrieval_recall=1.0,
        context_relevance_score=1.0,
        faithfulness_score=1.0,
        answer_relevance_score=1.0,
        answer_correctness_score=1.0,
        overall_score=1.0,
        hallucination_detected=False,
    ) == RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION
