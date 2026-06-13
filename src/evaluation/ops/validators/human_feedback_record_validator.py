from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.human_feedback_record_schema import (
    HUMAN_FEEDBACK_RECORD_SCHEMA,
)


class HumanFeedbackRecordValidator:
    """
    HumanFeedbackRecord validation service.
    """

    @staticmethod
    def validate(
        *,
        feedback_id: str,
        evaluator_id: str,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        model_name: str,
        created_at: datetime,
        sample_id: str | None,
        reviewer_id: str | None,
        rating: float | None,
        score: float | None,
        is_accepted: bool | None,
        comment: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "feedback_id": feedback_id,
                "evaluator_id": evaluator_id,
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "created_at": created_at,
                "sample_id": sample_id,
                "reviewer_id": reviewer_id,
                "rating": rating,
                "score": score,
                "is_accepted": is_accepted,
                "comment": comment,
                "notes": notes,
            },
            schema=HUMAN_FEEDBACK_RECORD_SCHEMA,
            error_factory=EvaluationValidationError,
        )