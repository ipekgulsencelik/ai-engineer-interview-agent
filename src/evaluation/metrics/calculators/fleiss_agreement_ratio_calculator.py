from __future__ import annotations

from collections import Counter
from collections.abc import Sequence


class FleissAgreementRatioCalculator:
    """
    Multi-rater raw agreement ratio calculator.

    For each sample, computes pairwise annotator agreement
    and averages it across all samples.
    """

    @staticmethod
    def calculate(
        *,
        label_matrix: Sequence[Sequence[str]],
    ) -> float:
        row_agreements = tuple(
            FleissAgreementRatioCalculator._row_agreement(
                labels=row,
            )
            for row in label_matrix
        )

        return sum(row_agreements) / len(row_agreements)

    @staticmethod
    def _row_agreement(
        *,
        labels: Sequence[str],
    ) -> float:
        evaluator_count = len(labels)

        counts = Counter(
            labels,
        )

        matching_pairs = sum(
            count * (count - 1)
            for count in counts.values()
        )

        possible_pairs = (
            evaluator_count
            * (evaluator_count - 1)
        )

        return matching_pairs / possible_pairs