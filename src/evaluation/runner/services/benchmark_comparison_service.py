from __future__ import annotations


class BenchmarkComparisonService:
    """
    Calculates benchmark comparison values.
    """

    def score_delta(
        self,
        *,
        baseline_score: float | None,
        candidate_score: float,
    ) -> float | None:
        if baseline_score is None:
            return None

        return candidate_score - baseline_score

    def winner(
        self,
        *,
        baseline_score: float | None,
        candidate_score: float,
    ) -> str | None:
        if baseline_score is None:
            return None

        if candidate_score > baseline_score:
            return "candidate"

        if candidate_score < baseline_score:
            return "baseline"

        return "tie"