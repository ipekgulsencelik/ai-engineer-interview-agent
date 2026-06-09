from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.metrics.constants.confidence_intervals import (
    DEFAULT_CONFIDENCE_LEVEL,
    DEFAULT_Z_SCORE,
)
from src.evaluation.metrics.validators.confidence_interval_input_validator import (
    ConfidenceIntervalInputValidator,
)
from src.evaluation.metrics.value_objects.confidence_interval import (
    ConfidenceInterval,
)


class ConfidenceIntervalCalculator:
    """
    Confidence interval calculation service.
    """

    def calculate(
        self,
        *,
        values: Sequence[float],
        confidence_level: float = (
            DEFAULT_CONFIDENCE_LEVEL
        ),
        z_score: float = (
            DEFAULT_Z_SCORE
        ),
    ) -> ConfidenceInterval:
        ConfidenceIntervalInputValidator.validate(
            values=values,
            confidence_level=confidence_level,
            z_score=z_score,
        )

        sample_mean = (
            self._calculate_mean(
                values,
            )
        )

        standard_error = (
            self._calculate_standard_error(
                values=values,
                sample_mean=sample_mean,
            )
        )

        margin_of_error = (
            z_score
            * standard_error
        )

        return ConfidenceInterval(
            lower_bound=(
                sample_mean
                - margin_of_error
            ),
            upper_bound=(
                sample_mean
                + margin_of_error
            ),
            confidence_level=confidence_level,
        )

    @staticmethod
    def _calculate_mean(
        values: Sequence[float],
    ) -> float:
        return sum(values) / len(values)

    @staticmethod
    def _calculate_standard_error(
        *,
        values: Sequence[float],
        sample_mean: float,
    ) -> float:
        if len(values) == 1:
            return 0.0

        variance = sum(
            (
                value
                - sample_mean
            )
            ** 2
            for value in values
        ) / (
            len(values)
            - 1
        )

        standard_deviation = (
            math.sqrt(
                variance,
            )
        )

        return (
            standard_deviation
            / math.sqrt(
                len(values),
            )
        )