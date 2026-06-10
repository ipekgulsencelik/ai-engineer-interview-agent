from __future__ import annotations

from statistics import stdev


class BootstrapStandardDeviationCalculator:
    """
    Calculates standard deviation for bootstrap statistic values.
    """

    @staticmethod
    def calculate(
        *,
        statistic_values: tuple[float, ...],
    ) -> float:
        if len(statistic_values) == 1:
            return 0.0

        return stdev(statistic_values)