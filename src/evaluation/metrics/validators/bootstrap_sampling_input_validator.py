from __future__ import annotations

import math
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.bootstrap import (
    MIN_BOOTSTRAP_ITERATIONS,
    MIN_BOOTSTRAP_SAMPLE_SIZE,
)


class BootstrapSamplingInputValidator:
    """
    Bootstrap sampling input validation service.
    """

    @staticmethod
    def validate(
        *,
        values: Sequence[float],
        bootstrap_iterations: int,
    ) -> None:
        if len(values) < MIN_BOOTSTRAP_SAMPLE_SIZE:
            raise EvaluationValidationError(
                "values cannot be empty."
            )

        if (
            isinstance(bootstrap_iterations, bool)
            or not isinstance(bootstrap_iterations, int)
        ):
            raise EvaluationValidationError(
                "bootstrap_iterations must be int."
            )

        if bootstrap_iterations < MIN_BOOTSTRAP_ITERATIONS:
            raise EvaluationValidationError(
                "bootstrap_iterations must be positive."
            )

        for index, value in enumerate(values):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
            ):
                raise EvaluationValidationError(
                    f"values[{index}] must be numeric."
                )

            if not math.isfinite(float(value)):
                raise EvaluationValidationError(
                    f"values[{index}] must be finite."
                )