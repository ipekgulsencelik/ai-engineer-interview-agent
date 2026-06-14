from __future__ import annotations

from src.evaluation.rag.services.rag_sample_evaluation_service import RAGSampleEvaluationService
from tests.evaluation.rag.factories import rag_sample


def test_rag_sample_evaluation_service_should_return_full_sample_level_result() -> None:
    result = RAGSampleEvaluationService().evaluate(
        experiment_id="experiment-1",
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="eval-a",
        sample=rag_sample(
            question="retrieval context",
            expected_context="retrieval context",
            expected_chunk_ids=("chunk-1",),
        ),
        generated_answer="retrieval context",
        retrieved_context="retrieval context",
        retrieved_chunk_ids=("chunk-1",),
    )

    assert result.experiment_id == "experiment-1"
    assert result.sample_id == "sample-1"
    assert result.retrieval_precision == 1.0
    assert result.retrieval_recall == 1.0
    assert result.context_relevance_score == 1.0
    assert result.faithfulness_score == 1.0
    assert result.passed is True
    assert result.latency_ms >= 0.0

from datetime import UTC, datetime


class _FixedClock:
    def __init__(self) -> None:
        self._values = iter(
            (
                datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC),
                datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC),
            )
        )

    def now(self) -> datetime:
        return next(self._values)


def test_rag_sample_evaluation_service_should_use_injected_clock_for_latency_and_created_at() -> None:
    result = RAGSampleEvaluationService(clock=_FixedClock()).evaluate(
        experiment_id="experiment-1",
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="eval-a",
        sample=rag_sample(
            question="retrieval context",
            expected_context="retrieval context",
            expected_chunk_ids=("chunk-1",),
        ),
        generated_answer="retrieval context",
        retrieved_context="retrieval context",
        retrieved_chunk_ids=("chunk-1",),
    )

    assert result.latency_ms == 1000.0
    assert result.created_at == datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC)
