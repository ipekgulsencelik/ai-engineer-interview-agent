from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.dashboard_trend_point_schema import (
    DASHBOARD_TREND_POINT_SCHEMA,
)


class DashboardTrendPointValidator:
    """
    DashboardTrendPoint validation service.
    """

    @staticmethod
    def validate(
        *,
        point_id: str,
        metric_name: str,
        value: float,
        occurred_at: datetime,
        unit: str | None,
        benchmark_id: str | None,
        experiment_id: str | None,
        model_name: str | None,
        label: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "point_id": point_id,
                "metric_name": metric_name,
                "value": value,
                "occurred_at": occurred_at,
                "unit": unit,
                "benchmark_id": benchmark_id,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "label": label,
                "notes": notes,
            },
            schema=DASHBOARD_TREND_POINT_SCHEMA,
            error_factory=EvaluationValidationError,
        )