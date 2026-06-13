from __future__ import annotations


class OnlineEvaluationPassEvaluator:
    """
    Evaluates whether an online metric passes
    the required production threshold.
    """

    @staticmethod
    def evaluate(
        *,
        metric_value: float,
        minimum_required_value: float,
    ) -> bool:
        return (
            metric_value
            >= minimum_required_value
        )