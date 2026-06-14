from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)
from src.evaluation.tracking.schemas.experiment_query_schema import (
    EXPERIMENT_QUERY_SCHEMA,
)


class ExperimentQueryValidator:
    """
    ExperimentQuery validation service.
    """

    @staticmethod
    def validate(
        *,
        experiment_id: str | None,
        run_id: str | None,
        experiment_name: str | None,
        experiment_version: str | None,
        dataset_id: str | None,
        dataset_name: str | None,
        dataset_version: str | None,
        benchmark_id: str | None,
        benchmark_name: str | None,
        benchmark_version: str | None,
        model_name: str | None,
        retriever_name: str | None,
        evaluator_name: str | None,
        status: ExperimentRunStatus | None,
        tag_key: str | None,
        tag_value: str | None,
        created_after: datetime | None,
        created_before: datetime | None,
        min_overall_score: float | None,
        max_overall_score: float | None,
        min_pass_rate: float | None,
        max_pass_rate: float | None,
        limit: int | None,
        offset: int | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "experiment_id": experiment_id,
                "run_id": run_id,
                "experiment_name": experiment_name,
                "experiment_version": experiment_version,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "dataset_version": dataset_version,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "status": (
                    None
                    if status is None
                    else str(status)
                ),
                "tag_key": tag_key,
                "tag_value": tag_value,
                "created_after": (
                    created_after
                    or datetime.min
                ),
                "created_before": (
                    created_before
                    or datetime.max
                ),
                "min_overall_score": min_overall_score,
                "max_overall_score": max_overall_score,
                "min_pass_rate": min_pass_rate,
                "max_pass_rate": max_pass_rate,
                "limit": limit,
                "offset": offset,
            },
            schema=EXPERIMENT_QUERY_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            status is not None
            and not isinstance(
                status,
                ExperimentRunStatus,
            )
        ):
            raise EvaluationValidationError(
                "status must be ExperimentRunStatus."
            )

        if (
            tag_key is None
            and tag_value is not None
        ):
            raise EvaluationValidationError(
                "tag_key is required when tag_value is provided."
            )

        if (
            created_after is not None
            and created_before is not None
            and created_after > created_before
        ):
            raise EvaluationValidationError(
                "created_after cannot be after created_before."
            )

        if (
            min_overall_score is not None
            and max_overall_score is not None
            and min_overall_score > max_overall_score
        ):
            raise EvaluationValidationError(
                "min_overall_score cannot be greater than max_overall_score."
            )

        if (
            min_pass_rate is not None
            and max_pass_rate is not None
            and min_pass_rate > max_pass_rate
        ):
            raise EvaluationValidationError(
                "min_pass_rate cannot be greater than max_pass_rate."
            )

        if (
            limit is not None
            and limit <= 0
        ):
            raise EvaluationValidationError(
                "limit must be greater than zero."
            )

        if (
            offset is not None
            and offset < 0
        ):
            raise EvaluationValidationError(
                "offset cannot be negative."
            )