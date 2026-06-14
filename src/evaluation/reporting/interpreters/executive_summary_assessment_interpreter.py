from __future__ import annotations


class ExecutiveSummaryAssessmentInterpreter:
    """
    Interprets overall score into executive assessment.
    """

    @staticmethod
    def interpret(
        *,
        overall_score: float,
    ) -> str:
        if overall_score >= 0.90:
            return "excellent"

        if overall_score >= 0.80:
            return "strong"

        if overall_score >= 0.70:
            return "acceptable"

        if overall_score >= 0.60:
            return "needs_improvement"

        return "high_risk"