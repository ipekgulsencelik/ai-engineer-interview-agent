from __future__ import annotations

from src.evaluation.rag.value_objects.rag_retrieval_metric_result import RAGRetrievalMetricResult


def test_rag_retrieval_metric_result_should_store_precision_and_recall() -> None:
    result = RAGRetrievalMetricResult(retrieval_precision=0.5, retrieval_recall=1.0)
    assert result.retrieval_precision == 0.5
    assert result.retrieval_recall == 1.0
