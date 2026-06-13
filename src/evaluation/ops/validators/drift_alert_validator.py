from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.constants.drift_alert import (
    ACKNOWLEDGED_AT_BEFORE_CREATED_AT_ERROR,
    ACKNOWLEDGED_AT_REQUIRED_ERROR,
    ACKNOWLEDGED_BY_REQUIRED_ERROR,
    ACKNOWLEDGED_FIELDS_NOT_ALLOWED_ERROR,
    ALERT_TRIGGER_MISMATCH_ERROR,
    DRIFT_DELTA_MISMATCH_ERROR,
    DRIFT_SEVERITY_TYPE_ERROR,
    NEGATIVE_DRIFT_THRESHOLD_ERROR,
)
from src.evaluation.ops.enums.drift_severity import (
    DriftSeverity,
)
from src.evaluation.ops.schemas.drift_alert_schema import (
    DRIFT_ALERT_SCHEMA,
)


class DriftAlertValidator:
    """
    DriftAlert validation service.
    """

    @staticmethod
    def validate(
        *,
        alert_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        experiment_id: str,
        model_name: str,
        baseline_score: float,
        current_score: float,
        drift_delta: float,
        drift_threshold: float,
        alert_triggered: bool,
        severity: DriftSeverity,
        interpretation: str,
        created_at: datetime,
        acknowledged: bool,
        acknowledged_by: str | None,
        acknowledged_at: datetime | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "alert_id": alert_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "baseline_score": baseline_score,
                "current_score": current_score,
                "drift_delta": drift_delta,
                "drift_threshold": drift_threshold,
                "alert_triggered": alert_triggered,
                "interpretation": interpretation,
                "created_at": created_at,
                "acknowledged": acknowledged,
                "acknowledged_by": acknowledged_by,
                "notes": notes,
            },
            schema=DRIFT_ALERT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            severity,
            DriftSeverity,
        ):
            raise EvaluationValidationError(
                DRIFT_SEVERITY_TYPE_ERROR
            )

        if drift_threshold < 0:
            raise EvaluationValidationError(
                NEGATIVE_DRIFT_THRESHOLD_ERROR
            )

        calculated_delta = (
            current_score
            - baseline_score
        )

        if abs(calculated_delta - drift_delta) > 1e-6:
            raise EvaluationValidationError(
                DRIFT_DELTA_MISMATCH_ERROR
            )

        expected_alert_triggered = (
            abs(drift_delta) >= drift_threshold
        )

        if alert_triggered != expected_alert_triggered:
            raise EvaluationValidationError(
                ALERT_TRIGGER_MISMATCH_ERROR
            )

        if acknowledged:
            if acknowledged_by is None:
                raise EvaluationValidationError(
                    ACKNOWLEDGED_BY_REQUIRED_ERROR
                )

            if acknowledged_at is None:
                raise EvaluationValidationError(
                    ACKNOWLEDGED_AT_REQUIRED_ERROR
                )

            if acknowledged_at < created_at:
                raise EvaluationValidationError(
                    ACKNOWLEDGED_AT_BEFORE_CREATED_AT_ERROR
                )

            return

        if (
            acknowledged_by is not None
            or acknowledged_at is not None
        ):
            raise EvaluationValidationError(
                ACKNOWLEDGED_FIELDS_NOT_ALLOWED_ERROR
            )