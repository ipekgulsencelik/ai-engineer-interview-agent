from __future__ import annotations

from collections.abc import Sequence


class AgreementRatioCalculator:
    """
    Raw agreement ratio calculator.
    """

    @staticmethod
    def calculate(
        *,
        evaluator_a_labels: Sequence[str],
        evaluator_b_labels: Sequence[str],
    ) -> float:
        matches = sum(
            left == right
            for left, right in zip(
                evaluator_a_labels,
                evaluator_b_labels,
                strict=True,
            )
        )

        return matches / len(
            evaluator_a_labels,
        )