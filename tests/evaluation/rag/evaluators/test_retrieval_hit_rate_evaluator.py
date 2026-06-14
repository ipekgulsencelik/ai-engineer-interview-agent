from __future__ import annotations

from src.evaluation.rag.evaluators.retrieval_hit_rate_evaluator import RetrievalHitRateEvaluator
from src.evaluation.rag.value_objects.retrieval_hit_rate_request import RetrievalHitRateRequest


def test_retrieval_hit_rate_evaluator_should_return_zero_when_expected_chunk_is_missing_from_top_k() -> None:
    request = RetrievalHitRateRequest(
        question="q",
        expected_chunk_id="chunk-2",
        retrieved_chunk_ids=("chunk-1",),
        top_k=1,
    )

    assert RetrievalHitRateEvaluator().evaluate(request=request) == 0.0


def test_retrieval_hit_rate_evaluator_should_return_one_when_expected_chunk_is_in_top_k() -> None:
    request = RetrievalHitRateRequest(
        question="q",
        expected_chunk_id="chunk-2",
        retrieved_chunk_ids=("chunk-1", "chunk-2"),
        top_k=2,
    )

    assert RetrievalHitRateEvaluator().evaluate(request=request) == 1.0
