from __future__ import annotations

from datetime import UTC, datetime

from src.evaluation.rag.factories.rag_evaluation_result_factory import RAGEvaluationResultFactory
from tests.evaluation.rag.factories import rag_sample


def test_rag_evaluation_result_factory_should_copy_sample_identity_and_scores() -> None:
    sample = rag_sample(sample_id="sample-x", benchmark_id="benchmark-x")
    result = RAGEvaluationResultFactory.create(
        experiment_id="experiment-1",
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="evaluator-a",
        sample=sample,
        generated_answer="answer",
        retrieved_context_count=1,
        relevant_context_count=1,
        retrieval_precision=1.0,
        retrieval_recall=1.0,
        context_relevance_score=1.0,
        faithfulness_score=1.0,
        answer_relevance_score=1.0,
        answer_correctness_score=1.0,
        overall_score=1.0,
        hallucination_detected=False,
        passed=True,
        latency_ms=1.0,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        interpretation="passed",
    )

    assert result.sample_id == "sample-x"
    assert result.benchmark_id == "benchmark-x"
    assert result.overall_score == 1.0
