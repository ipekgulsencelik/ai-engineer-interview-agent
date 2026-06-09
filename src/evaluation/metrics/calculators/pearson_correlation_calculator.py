from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.pearson_coefficient_calculator import (
    PearsonCoefficientCalculator,
)
from src.evaluation.metrics.constants.correlations import (
    DEFAULT_SIGNIFICANCE_LEVEL,
    P_VALUE_MAX,
    PEARSON_METHOD_NAME,
)
from src.evaluation.metrics.interpreters.correlation_interpreter import (
    CorrelationInterpreter,
)
from src.evaluation.metrics.validators.correlation_input_validator import (
    CorrelationInputValidator,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)


class PearsonCorrelationCalculator:
    """
    Pearson correlation calculation service.
    """

    @staticmethod
    def calculate(
        *,
        metric_x: str,
        metric_y: str,
        x_values: Sequence[float],
        y_values: Sequence[float],
        p_value: float = P_VALUE_MAX,
    ) -> CorrelationResult:
        CorrelationInputValidator.validate(
            x_values=x_values,
            y_values=y_values,
        )

        correlation_coefficient = PearsonCoefficientCalculator.calculate(
            x_values=x_values,
            y_values=y_values,
        )

        return CorrelationResult(
            metric_x=metric_x,
            metric_y=metric_y,
            correlation_coefficient=correlation_coefficient,
            p_value=p_value,
            sample_count=len(x_values),
            method=PEARSON_METHOD_NAME,
            is_significant=(
                p_value
                < DEFAULT_SIGNIFICANCE_LEVEL
            ),
            interpretation=CorrelationInterpreter.interpret(
                correlation_coefficient=correlation_coefficient,
            ),
        )