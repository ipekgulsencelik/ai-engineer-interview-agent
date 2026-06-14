from __future__ import annotations


class ExperimentComparisonInterpreter:
    """
    Interprets experiment comparison deltas.
    """

    @staticmethod
    def interpret(
        *,
        overall_score_delta: float | None,
        pass_rate_delta: float | None,
    ) -> str:
        if overall_score_delta is None:
            return "experiment_comparison_inconclusive"

        if overall_score_delta > 0:
            return "candidate_experiment_improved"

        if overall_score_delta < 0:
            return "candidate_experiment_regressed"

        if (
            pass_rate_delta is not None
            and pass_rate_delta > 0
        ):
            return "candidate_pass_rate_improved"

        if (
            pass_rate_delta is not None
            and pass_rate_delta < 0
        ):
            return "candidate_pass_rate_regressed"

        return "experiment_comparison_unchanged"