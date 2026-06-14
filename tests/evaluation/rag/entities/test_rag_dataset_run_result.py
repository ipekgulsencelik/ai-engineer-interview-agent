from __future__ import annotations

from datetime import UTC, datetime

from src.evaluation.rag.entities.rag_dataset_run_result import RAGDatasetRunResult
from tests.evaluation.rag.factories import rag_report


def test_rag_dataset_run_result_should_expose_passed_and_failed_properties() -> None:
    run = RAGDatasetRunResult(
        run_id="run-1",
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_name="Benchmark",
        benchmark_version="1.0.0",
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="evaluator-a",
        report=rag_report(),
        sample_count=1,
        passed_count=1,
        failed_count=0,
        pass_rate=1.0,
        overall_score=0.8,
        started_at=datetime(2026, 1, 1, tzinfo=UTC),
        completed_at=datetime(2026, 1, 1, tzinfo=UTC),
        duration_ms=0.0,
        interpretation="passed",
    )

    assert run.passed is True
    assert run.failed is False
