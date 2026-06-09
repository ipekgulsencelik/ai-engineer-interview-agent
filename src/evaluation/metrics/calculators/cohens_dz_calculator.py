from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.sample_standard_deviation_calculator import (
    SampleStandardDeviationCalculator,
)
from src.evaluation.metrics.constants.statistical_tests import (
    ZERO_STANDARD_DEVIATION_THRESHOLD,
)


class CohensDzCalculator:
    """
    Cohen's dz effect size calculator for paired samples.
    """

    @staticmethod
    def calculate(
        *,
        differences: Sequence[float],
    ) -> float:
        mean_difference = sum(
            differences,
        ) / len(
            differences,
        )

        standard_deviation = SampleStandardDeviationCalculator.calculate(
            values=differences,
        )

        if abs(
            standard_deviation,
        ) < ZERO_STANDARD_DEVIATION_THRESHOLD:
            raise EvaluationValidationError(
                "Cohen's dz is undefined when differences are constant."
            )

        return (
            mean_difference
            / standard_deviation
        )