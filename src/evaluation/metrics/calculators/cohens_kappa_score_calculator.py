from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.agreements import (
    KAPPA_ZERO_DENOMINATOR_THRESHOLD,
)


class CohensKappaScoreCalculator:
    """
    Cohen's kappa score calculator.
    """

    @staticmethod
    def calculate(
        *,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
        agreement_ratio: float,
    ) -> float:
        labels = set(
            evaluator_a_labels,
        ) | set(
            evaluator_b_labels,
        )

        evaluator_a_counts = Counter(
            evaluator_a_labels,
        )
        evaluator_b_counts = Counter(
            evaluator_b_labels,
        )

        total = len(
            evaluator_a_labels,
        )

        expected_agreement = sum(
            (
                evaluator_a_counts[label]
                / total
            )
            * (
                evaluator_b_counts[label]
                / total
            )
            for label in labels
        )

        denominator = (
            1.0
            - expected_agreement
        )

        if abs(
            denominator,
        ) < KAPPA_ZERO_DENOMINATOR_THRESHOLD:
            raise EvaluationValidationError(
                "Cohen kappa is undefined when expected agreement is 1.0."
            )

        return (
            agreement_ratio
            - expected_agreement
        ) / denominator