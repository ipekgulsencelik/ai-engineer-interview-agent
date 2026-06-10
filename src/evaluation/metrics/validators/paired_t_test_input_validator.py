from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.statistical_tests import (
    MAX_ALPHA,
    MAX_P_VALUE,
    MIN_ALPHA,
    MIN_PAIRED_T_TEST_SAMPLE_COUNT,
    MIN_P_VALUE,
)


class PairedTTestInputValidator:
    """
    Paired t-test input validation service.
    """

    @staticmethod
    def validate(
        *,
        before_values: Sequence[float],
        after_values: Sequence[float],
        p_value: float,
        alpha: float,
    ) -> None:
        if len(before_values) != len(after_values):
            raise EvaluationValidationError(
                "before_values and after_values must have the same length."
            )

        if len(before_values) < MIN_PAIRED_T_TEST_SAMPLE_COUNT:
            raise EvaluationValidationError(
                "paired t-test requires at least "
                f"{MIN_PAIRED_T_TEST_SAMPLE_COUNT} paired observations."
            )

        PairedTTestInputValidator._validate_numeric_series(
            values=before_values,
            field_name="before_values",
        )

        PairedTTestInputValidator._validate_numeric_series(
            values=after_values,
            field_name="after_values",
        )

        if not (
            MIN_P_VALUE
            <= p_value
            <= MAX_P_VALUE
        ):
            raise EvaluationValidationError(
                "p_value must be between 0.0 and 1.0."
            )

        if not (
            MIN_ALPHA
            < alpha
            < MAX_ALPHA
        ):
            raise EvaluationValidationError(
                "alpha must be between 0.0 and 1.0."
            )

    @staticmethod
    def _validate_numeric_series(
        *,
        values: Sequence[float],
        field_name: str,
    ) -> None:
        for index, value in enumerate(values):
            if (
                isinstance(value, bool)
                or not isinstance(
                    value,
                    (int, float),
                )
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be numeric."
                )

            if not math.isfinite(
                float(value),
            ):
                raise EvaluationValidationError(
                    f"{field_name}[{index}] must be finite."
                )