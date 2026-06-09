from __future__ import annotations

import math
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


class PairedTStatisticCalculator:
    """
    Paired t-statistic calculator.
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
                "paired t-test is undefined when differences are constant."
            )

        standard_error = standard_deviation / math.sqrt(
            len(differences),
        )

        return (
            mean_difference
            / standard_error
        )