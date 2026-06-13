from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.constants.dashboard_metric_card import (
    DASHBOARD_SEVERITY_TYPE_ERROR,
    NEGATIVE_SORT_ORDER_ERROR,
    TREND_VALUE_LABEL_MISMATCH_ERROR,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)
from src.evaluation.ops.schemas.dashboard_metric_card_schema import (
    DASHBOARD_METRIC_CARD_SCHEMA,
)


class DashboardMetricCardValidator:
    """
    DashboardMetricCard validation service.
    """

    @staticmethod
    def validate(
        *,
        card_id: str,
        title: str,
        value: float,
        formatted_value: str,
        unit: str | None,
        description: str | None,
        trend_value: float | None,
        trend_label: str | None,
        is_positive_trend: bool | None,
        severity: (DashboardSeverity | None),
        sort_order: int,
    ) -> None:
        SchemaValidator.validate(
            values={
                "card_id": card_id,
                "title": title,
                "value": value,
                "formatted_value": (formatted_value),
                "unit": unit,
                "description": (description),
                "trend_value": (trend_value),
                "trend_label": (trend_label),
                "is_positive_trend": (is_positive_trend),
                "severity": severity,
                "sort_order": sort_order,
            },
            schema=(DASHBOARD_METRIC_CARD_SCHEMA),
            error_factory=(EvaluationValidationError),
        )

        if severity is not None and not isinstance(
            severity,
            DashboardSeverity,
        ):
            raise EvaluationValidationError(DASHBOARD_SEVERITY_TYPE_ERROR)

        if trend_label is not None and trend_value is None:
            raise EvaluationValidationError(TREND_VALUE_LABEL_MISMATCH_ERROR)

        if sort_order < 0:
            raise EvaluationValidationError(NEGATIVE_SORT_ORDER_ERROR)
