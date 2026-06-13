from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.ops.entities.human_feedback_record import (
    HumanFeedbackRecord,
)


class HumanFeedbackRecordFactory:
    """
    Creates human feedback records.
    """

    @staticmethod
    def create(
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
        created_at: datetime | None = None,
        notes: str | None = None,
    ) -> HumanFeedbackRecord:
        return HumanFeedbackRecord(
            feedback_id=str(
                uuid4(),
            ),
            evaluator_id=evaluator_id,
            experiment_id=experiment_id,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            model_name=model_name,
            created_at=(created_at or datetime.now(UTC)),
            sample_id=sample_id,
            reviewer_id=reviewer_id,
            rating=rating,
            score=score,
            is_accepted=is_accepted,
            comment=comment,
            notes=notes,
        )
