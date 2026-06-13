from __future__ import annotations


class OnlineEvaluationInterpreter:
    """
    Builds interpretation labels for online
    evaluation results.
    """

    @staticmethod
    def interpret(
        *,
        passed: bool,
    ) -> str:
        if passed:
            return "online_evaluation_passed"

        return "online_evaluation_failed"