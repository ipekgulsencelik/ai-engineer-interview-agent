from __future__ import annotations


class BenchmarkPassRateCalculator:
    """
    Calculates benchmark pass rate.
    """

    def calculate(
        self,
        *,
        sample_count: int,
        passed_count: int,
    ) -> float:
        if sample_count == 0:
            return 0.0

        return passed_count / sample_count