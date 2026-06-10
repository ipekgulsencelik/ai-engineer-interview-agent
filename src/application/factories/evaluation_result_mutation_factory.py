from __future__ import annotations

from dataclasses import replace

from src.domain.results.evaluation_result import (
    EvaluationResult,
)


class EvaluationResultMutationFactory:
    """
    Immutable EvaluationResult update helper.
    """

    @staticmethod
    def with_latency_seconds(
        *,
        result: EvaluationResult,
        latency_seconds: float,
    ) -> EvaluationResult:
        return replace(
            result,
            metadata=replace(
                result.metadata,
                latency_seconds=latency_seconds,
            ),
        )