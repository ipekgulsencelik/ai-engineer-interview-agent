from __future__ import annotations

from src.evaluation.metrics.constants.benchmark_trends import (
    DEGRADING_TREND_DIRECTION,
    IMPROVING_TREND_DIRECTION,
    STABLE_TREND_DIRECTION,
)


class BenchmarkTrendDetector:
    """
    Detects benchmark score trend direction.
    """

    @staticmethod
    def detect(
        *,
        scores: tuple[float, ...],
    ) -> str:
        if len(scores) < 2:
            return STABLE_TREND_DIRECTION

        first_score = scores[0]
        last_score = scores[-1]

        if last_score > first_score:
            return IMPROVING_TREND_DIRECTION

        if last_score < first_score:
            return DEGRADING_TREND_DIRECTION

        return STABLE_TREND_DIRECTION