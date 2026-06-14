from __future__ import annotations


class ExperimentDeltaCalculator:
    """
    Calculates numeric deltas between baseline
    and candidate experiment values.
    """

    @staticmethod
    def float_delta(
        *,
        baseline_value: float | None,
        candidate_value: float | None,
    ) -> float | None:
        if (
            baseline_value is None
            or candidate_value is None
        ):
            return None

        return (
            candidate_value
            - baseline_value
        )

    @staticmethod
    def int_delta(
        *,
        baseline_value: int | None,
        candidate_value: int | None,
    ) -> int | None:
        if (
            baseline_value is None
            or candidate_value is None
        ):
            return None

        return (
            candidate_value
            - baseline_value
        )