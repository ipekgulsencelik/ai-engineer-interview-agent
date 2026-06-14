from __future__ import annotations

from datetime import UTC, datetime

from src.evaluation.rag.factories.rag_dataset_run_result_factory import RAGDatasetRunResultFactory
from tests.evaluation.rag.factories import rag_report


def test_rag_dataset_run_result_factory_should_copy_report_counts_and_duration() -> None:
    started_at = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    completed_at = datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC)
    result = RAGDatasetRunResultFactory.create(
        experiment_id="experiment-1",
        model_name="model-a",
        retriever_name="retriever-a",
        evaluator_name="evaluator-a",
        report=rag_report(),
        started_at=started_at,
        completed_at=completed_at,
    )

    assert result.sample_count == 1
    assert result.failed_count == 0
    assert result.duration_ms == 2000.0
    assert result.failed is False
