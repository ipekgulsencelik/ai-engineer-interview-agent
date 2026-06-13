from __future__ import annotations


class DriftDeltaCalculator:
    """
    Calculates evaluation drift deltas.
    """

    @staticmethod
    def calculate(
        *,
        baseline_score: float,
        current_score: float,
    ) -> float:
        return (
            current_score
            - baseline_score
        )