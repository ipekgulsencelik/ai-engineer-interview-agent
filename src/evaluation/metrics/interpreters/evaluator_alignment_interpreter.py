from __future__ import annotations


class EvaluatorAlignmentInterpreter:
    """
    Converts evaluator alignment score into interpretation label.
    """

    @staticmethod
    def interpret(
        score: float,
    ) -> str:
        if score >= 0.90:
            return "excellent_alignment"

        if score >= 0.75:
            return "high_alignment"

        if score >= 0.50:
            return "moderate_alignment"

        return "low_alignment"