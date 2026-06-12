from __future__ import annotations


class CIPolicyEvaluator:
    """
    Evaluates overall CI policy outcome.
    """

    @staticmethod
    def evaluate(
        *,
        blocking_failure_count: int,
    ) -> bool:
        return (
            blocking_failure_count == 0
        )