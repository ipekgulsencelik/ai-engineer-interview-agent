from __future__ import annotations

from src.evaluation.rag.services.rag_retrieval_metric_service import RAGRetrievalMetricService
from tests.evaluation.rag.factories import rag_sample


def test_rag_retrieval_metric_service_should_score_expected_chunk_hit() -> None:
    result = RAGRetrievalMetricService().evaluate(
        sample=rag_sample(expected_chunk_ids=("chunk-2",), expected_context="context"),
        generated_answer="answer",
        retrieved_context="context",
        retrieved_chunk_ids=("chunk-1", "chunk-2"),
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="eval-a",
    )

    assert result.retrieval_precision == 1.0
    assert result.retrieval_recall == 1.0


def test_rag_retrieval_metric_service_should_score_expected_chunk_miss_independent_of_context_recall() -> None:
    result = RAGRetrievalMetricService().evaluate(
        sample=rag_sample(expected_chunk_ids=("chunk-3",), expected_context="context"),
        generated_answer="answer",
        retrieved_context="context",
        retrieved_chunk_ids=("chunk-1", "chunk-2"),
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="eval-a",
    )

    assert result.retrieval_precision == 0.0
    assert result.retrieval_recall == 1.0
