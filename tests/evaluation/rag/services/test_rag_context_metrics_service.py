from __future__ import annotations

from src.evaluation.rag.services.rag_context_metrics_service import RAGContextMetricsService
from tests.evaluation.rag.factories import rag_sample


def test_rag_context_metrics_service_should_evaluate_context_recall() -> None:
    score = RAGContextMetricsService().evaluate_context_recall(
        sample=rag_sample(expected_context="context"),
        generated_answer="answer",
        retrieved_context="context",
        model_name="model-a",
        evaluator_name="evaluator-a",
    )

    assert score == 1.0


def test_rag_context_metrics_service_should_evaluate_retrieval_hit_rate() -> None:
    score = RAGContextMetricsService().evaluate_retrieval_hit_rate(
        sample=rag_sample(expected_chunk_ids=("c1",)),
        retrieved_chunk_ids=("c1",),
        model_name="model-a",
        retriever_name="retriever-a",
    )

    assert score == 1.0
