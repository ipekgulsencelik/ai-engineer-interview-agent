from __future__ import annotations

from collections.abc import Iterable

from src.evaluation.ops.factories.human_feedback_record_factory import (
    HumanFeedbackRecordFactory,
)
from src.evaluation.ops.entities.human_feedback_record import (
    HumanFeedbackRecord,
)


class HumanFeedbackIngestionService:
    """
    Human feedback ingestion orchestration service.
    """

    def __init__(
        self,
        *,
        record_factory: (HumanFeedbackRecordFactory | None) = None,
    ) -> None:
        self._record_factory = record_factory or HumanFeedbackRecordFactory()

    def ingest(
        self,
        *,
        evaluator_id: str,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        model_name: str,
        sample_id: str | None = None,
        reviewer_id: str | None = None,
        rating: float | None = None,
        score: float | None = None,
        is_accepted: bool | None = None,
        comment: str | None = None,
        notes: str | None = None,
    ) -> HumanFeedbackRecord:
        return self._record_factory.create(
            evaluator_id=evaluator_id,
            experiment_id=experiment_id,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            sample_id=sample_id,
            reviewer_id=reviewer_id,
            rating=rating,
            score=score,
            is_accepted=is_accepted,
            comment=comment,
            notes=notes,
        )

    def ingest_batch(
        self,
        *,
        records: Iterable[HumanFeedbackRecord],
    ) -> tuple[
        HumanFeedbackRecord,
        ...,
    ]:
        return tuple(
            records,
        )
