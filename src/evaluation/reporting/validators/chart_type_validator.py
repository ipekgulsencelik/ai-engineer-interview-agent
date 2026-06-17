from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class ChartTypeValidator:
    """
    Validates supported chart types.
    """

    SUPPORTED_CHART_TYPES = frozenset(
        {
            "line",
            "bar",
            "pie",
            "scatter",
        }
    )

    def validate(
        self,
        *,
        chart_type: str,
    ) -> None:
        if chart_type not in self.SUPPORTED_CHART_TYPES:
            raise EvaluationValidationError(
                f"Unsupported chart type: {chart_type}",
            )