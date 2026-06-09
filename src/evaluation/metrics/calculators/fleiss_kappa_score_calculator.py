from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.agreements import (
    KAPPA_ZERO_DENOMINATOR_THRESHOLD,
)


class FleissKappaScoreCalculator:
    """
    Fleiss kappa score calculator.
    """

    @staticmethod
    def calculate(
        *,
        label_matrix: Sequence[Sequence[str]],
        agreement_ratio: float,
    ) -> float:
        sample_count = len(label_matrix)
        evaluator_count = len(label_matrix[0])

        labels = sorted(
            {
                label
                for row in label_matrix
                for label in row
            }
        )

        category_proportions = {
            label: (
                sum(
                    row.count(label)
                    for row in label_matrix
                )
                / (
                    sample_count
                    * evaluator_count
                )
            )
            for label in labels
        }

        expected_agreement = sum(
            proportion ** 2
            for proportion in category_proportions.values()
        )

        denominator = (
            1.0
            - expected_agreement
        )

        if abs(
            denominator,
        ) < KAPPA_ZERO_DENOMINATOR_THRESHOLD:
            raise EvaluationValidationError(
                "Fleiss kappa is undefined when expected agreement is 1.0."
            )

        return (
            agreement_ratio
            - expected_agreement
        ) / denominator