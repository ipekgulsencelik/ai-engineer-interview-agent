from __future__ import annotations


class DistributionDriftCalculator:
    """
    Calculates normalized drift between two distributions.
    """

    @staticmethod
    def calculate(
        *,
        baseline_distribution: dict[str, int],
        comparison_distribution: dict[str, int],
    ) -> dict[str, float]:
        keys = set(
            baseline_distribution,
        ) | set(
            comparison_distribution,
        )

        baseline_total = sum(
            baseline_distribution.values(),
        )
        comparison_total = sum(
            comparison_distribution.values(),
        )

        if baseline_total == 0 or comparison_total == 0:
            return {
                key: 0.0
                for key in sorted(keys)
            }

        return {
            key: abs(
                (
                    baseline_distribution.get(
                        key,
                        0,
                    )
                    / baseline_total
                )
                - (
                    comparison_distribution.get(
                        key,
                        0,
                    )
                    / comparison_total
                )
            )
            for key in sorted(keys)
        }