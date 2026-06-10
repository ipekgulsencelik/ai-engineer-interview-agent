from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)


class CorrelationAnalysisService:
    """
    Correlation analytics facade.
    """

    def __init__(
        self,
        *,
        pearson_calculator: (
            PearsonCorrelationCalculator | None
        ) = None,
    ) -> None:
        self._pearson_calculator = (
            pearson_calculator
            or PearsonCorrelationCalculator()
        )

    def analyze_pearson(
        self,
        *,
        metric_x: str,
        metric_y: str,
        x_values: Sequence[float],
        y_values: Sequence[float],
        p_value: float = 1.0,
    ) -> CorrelationResult:
        return self._pearson_calculator.calculate(
            metric_x=metric_x,
            metric_y=metric_y,
            x_values=x_values,
            y_values=y_values,
            p_value=p_value,
        )