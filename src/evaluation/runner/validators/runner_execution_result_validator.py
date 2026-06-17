from __future__ import annotations

from datetime import datetime
from math import isfinite

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.runner.schemas.runner_execution_result_schema import (
    RUNNER_EXECUTION_RESULT_SCHEMA,
)


class RunnerExecutionResultValidator:
    """
    RunnerExecutionResult validation service.
    """

    SUPPORTED_STATUSES = frozenset(
        {
            "pending",
            "running",
            "success",
            "failed",
            "cancelled",
            "skipped",
            "timeout",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        execution_id: str,
        runner_id: str,
        runner_name: str,
        status: str,
        started_at: datetime,
        completed_at: datetime | None,
        duration_ms: float | None,
        success: bool,
        score: float | None,
        error_message: str | None,
        retry_count: int,
        output_uri: str | None,
        artifact_id: str | None,
        report_id: str | None,
        dataset_id: str | None,
        run_id: str | None,
        experiment_id: str | None,
        worker_id: str | None,
        correlation_id: str | None,
        trace_id: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "execution_id": execution_id,
                "runner_id": runner_id,
                "runner_name": runner_name,
                "status": status,
                "started_at": started_at,
                "completed_at": (
                    completed_at
                    or datetime.max
                ),
                "duration_ms": duration_ms,
                "success": success,
                "score": score,
                "error_message": error_message,
                "retry_count": retry_count,
                "output_uri": output_uri,
                "artifact_id": artifact_id,
                "report_id": report_id,
                "dataset_id": dataset_id,
                "run_id": run_id,
                "experiment_id": experiment_id,
                "worker_id": worker_id,
                "correlation_id": correlation_id,
                "trace_id": trace_id,
                "metadata": metadata or {},
            },
            schema=RUNNER_EXECUTION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if status not in cls.SUPPORTED_STATUSES:
            raise EvaluationValidationError(
                "status must be one of: pending, running, success, "
                "failed, cancelled, skipped, timeout."
            )

        if completed_at is not None and completed_at < started_at:
            raise EvaluationValidationError(
                "completed_at cannot be before started_at."
            )

        if duration_ms is not None:
            if not isinstance(
                duration_ms,
                int | float,
            ) or not isfinite(
                float(
                    duration_ms,
                )
            ):
                raise EvaluationValidationError(
                    "duration_ms must be finite numeric value."
                )

            if duration_ms < 0:
                raise EvaluationValidationError(
                    "duration_ms cannot be negative."
                )

        if score is not None:
            if not isinstance(
                score,
                int | float,
            ) or not isfinite(
                float(
                    score,
                )
            ):
                raise EvaluationValidationError(
                    "score must be finite numeric value."
                )

        if success and error_message is not None:
            raise EvaluationValidationError(
                "error_message must be None when success is True."
            )

        if status == "success" and not success:
            raise EvaluationValidationError(
                "success must be True when status is success."
            )

        if status in {
            "failed",
            "timeout",
        } and error_message is None:
            raise EvaluationValidationError(
                "error_message is required for failed or timeout status."
            )

        if metadata is not None:
            for key, value in metadata.items():
                if not isinstance(
                    key,
                    str,
                ) or not key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )