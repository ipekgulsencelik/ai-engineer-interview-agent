from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.calculators.mae_calculator import (
    MAECalculator,
)
from src.evaluation.metrics.calculators.mse_calculator import (
    MSECalculator,
)
from src.evaluation.metrics.calculators.r2_score_calculator import (
    R2ScoreCalculator,
)
from src.evaluation.metrics.calculators.rmse_calculator import (
    RMSECalculator,
)
from src.evaluation.metrics.constants.regression_metrics import (
    DEFAULT_ACCEPTABLE_R2_THRESHOLD,
)
from src.evaluation.metrics.interpreters.regression_metric_interpreter import (
    RegressionMetricInterpreter,
)
from src.evaluation.metrics.validators.regression_input_validator import (
    RegressionInputValidator,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


class RegressionMetricsCalculator:
    """
    Regression metrics facade calculator.
    """

    @staticmethod
    def calculate(
        *,
        metric_name: str,
        actual_values: Sequence[float],
        predicted_values: Sequence[float],
        notes: str | None = None,
    ) -> RegressionMetricResult:
        RegressionInputValidator.validate(
            actual_values=actual_values,
            predicted_values=predicted_values,
        )

        mae = MAECalculator.calculate(
            actual_values=actual_values,
            predicted_values=predicted_values,
        )

        mse = MSECalculator.calculate(
            actual_values=actual_values,
            predicted_values=predicted_values,
        )

        rmse = RMSECalculator.calculate(
            mse=mse,
        )

        r2_score = R2ScoreCalculator.calculate(
            actual_values=actual_values,
            predicted_values=predicted_values,
        )

        return RegressionMetricResult(
            metric_name=metric_name,
            mae=mae,
            mse=mse,
            rmse=rmse,
            r2_score=r2_score,
            sample_count=len(actual_values),
            is_acceptable=(
                r2_score
                >= DEFAULT_ACCEPTABLE_R2_THRESHOLD
            ),
            interpretation=RegressionMetricInterpreter.interpret(
                r2_score=r2_score,
            ),
            notes=notes,
        )