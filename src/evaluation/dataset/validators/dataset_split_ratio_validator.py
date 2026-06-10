from __future__ import annotations

import math

from src.evaluation.dataset.constants.dataset_splits import (
    SPLIT_RATIO_SUM_TARGET,
    SPLIT_RATIO_TOLERANCE,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)


class DatasetSplitRatioValidator:
    """
    Dataset split ratio validation service.
    """

    @staticmethod
    def validate(
        *,
        train_ratio: float,
        validation_ratio: float,
        test_ratio: float,
    ) -> None:
        ratios = (
            train_ratio,
            validation_ratio,
            test_ratio,
        )

        for ratio in ratios:
            if not isinstance(ratio, (int, float)) or isinstance(ratio, bool):
                raise EvaluationValidationError(
                    "split ratios must be numeric."
                )

            if ratio < 0 or ratio > 1:
                raise EvaluationValidationError(
                    "split ratios must be between 0 and 1."
                )

        total = train_ratio + validation_ratio + test_ratio

        if not math.isclose(
            total,
            SPLIT_RATIO_SUM_TARGET,
            rel_tol=SPLIT_RATIO_TOLERANCE,
            abs_tol=SPLIT_RATIO_TOLERANCE,
        ):
            raise EvaluationValidationError(
                "split ratios must sum to 1.0."
            )