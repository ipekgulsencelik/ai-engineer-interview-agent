from __future__ import annotations


class QualityGateEvaluator:
    """
    Evaluates quality gate pass/fail state.
    """

    @staticmethod
    def evaluate(
        *,
        score: float,
        minimum_required_score: float,
    ) -> bool:
        return (
            score
            >= minimum_required_score
        )