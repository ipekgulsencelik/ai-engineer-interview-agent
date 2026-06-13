from __future__ import annotations

from src.evaluation.ops.entities.human_feedback_record import HumanFeedbackRecord
from src.evaluation.ops.services.human_feedback_ingestion_service import (
    HumanFeedbackIngestionService,
)


def test_human_feedback_ingestion_service_should_create_feedback_record() -> None:
    record = HumanFeedbackIngestionService().ingest(
        evaluator_id="evaluator-1",
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        model_name="gpt-5",
        sample_id="sample-1",
        reviewer_id="reviewer-1",
        rating=0.90,
        score=0.88,
        is_accepted=True,
        comment="Looks aligned.",
        notes="human review",
    )

    assert isinstance(record, HumanFeedbackRecord)
    assert record.feedback_id
    assert record.has_rating is True
    assert record.has_score is True
    assert record.has_comment is True
    assert record.has_reviewer is True
    assert record.is_accepted is True
    assert record.notes == "human review"


def test_human_feedback_ingestion_service_should_preserve_batch_records() -> None:
    service = HumanFeedbackIngestionService()
    first = service.ingest(
        evaluator_id="evaluator-1",
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        model_name="gpt-5",
    )
    second = service.ingest(
        evaluator_id="evaluator-1",
        experiment_id="experiment-2",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        model_name="gpt-5",
    )

    assert service.ingest_batch(records=[first, second]) == (first, second)
