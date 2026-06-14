from __future__ import annotations


class ExperimentTrendDeltaCalculator:
    """
    Calculates trend deltas.
    """

    @staticmethod
    def calculate(
        *,
        first_value: float | None,
        latest_value: float | None,
    ) -> float | None:
        if (
            first_value is None
            or latest_value is None
        ):
            return None

        return (
            latest_value
            - first_value
        )