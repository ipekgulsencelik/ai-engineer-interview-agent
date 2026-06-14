from __future__ import annotations

from src.evaluation.rag.value_objects.rag_metric_evaluation_result import RAGMetricEvaluationResult


def test_rag_metric_evaluation_result_should_alias_context_relevance_and_answer_correctness() -> None:
    result = RAGMetricEvaluationResult(faithfulness_score=0.8, answer_relevance_score=0.7, context_precision_score=0.6)
    assert result.context_relevance_score == 0.6
    assert result.answer_correctness_score == 0.7
