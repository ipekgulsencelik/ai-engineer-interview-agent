from __future__ import annotations

from datetime import datetime
from math import isfinite

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.telemetry_metric_schema import (
    TELEMETRY_METRIC_SCHEMA,
)


class TelemetryMetricValidator:
    """
    TelemetryMetric validation service.
    """

    @staticmethod
    def validate(
        *,
        metric_id: str,
        metric_name: str,
        metric_value: float,
        unit: str,
        source: str,
        recorded_at: datetime,
        labels: dict[
            str,
            str,
        ],
        tenant_id: str | None,
        experiment_id: str | None,
        run_id: str | None,
        report_id: str | None,
        artifact_id: str | None,
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
                "metric_id": metric_id,
                "metric_name": metric_name,
                "metric_value": str(
                    metric_value,
                ),
                "unit": unit,
                "source": source,
                "recorded_at": recorded_at,
                "labels": labels,
                "tenant_id": tenant_id,
                "experiment_id": experiment_id,
                "run_id": run_id,
                "report_id": report_id,
                "artifact_id": artifact_id,
                "worker_id": worker_id,
                "correlation_id": correlation_id,
                "trace_id": trace_id,
                "metadata": metadata or {},
            },
            schema=TELEMETRY_METRIC_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            metric_value,
            int | float,
        ):
            raise EvaluationValidationError(
                "metric_value must be numeric."
            )

        if not isfinite(
            float(
                metric_value,
            )
        ):
            raise EvaluationValidationError(
                "metric_value must be finite."
            )

        TelemetryMetricValidator._validate_string_dict(
            value=labels,
            field_name="labels",
        )

        if metadata is not None:
            TelemetryMetricValidator._validate_string_dict(
                value=metadata,
                field_name="metadata",
            )

    @staticmethod
    def _validate_string_dict(
        *,
        value: dict[
            str,
            str,
        ],
        field_name: str,
    ) -> None:
        for key, item in value.items():
            if (
                not isinstance(
                    key,
                    str,
                )
                or not key.strip()
            ):
                raise EvaluationValidationError(
                    f"{field_name} keys must be non-empty strings."
                )

            if not isinstance(
                item,
                str,
            ):
                raise EvaluationValidationError(
                    f"{field_name} values must be strings."
                )