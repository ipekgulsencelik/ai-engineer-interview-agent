from __future__ import annotations

from src.evaluation.reporting.enums.summary_trend_direction import (
    SummaryTrendDirection,
)


class VisualTrendDirectionDetector:
    """
    Infers visual trend direction from score sequence.
    """

    @staticmethod
    def detect(
        *,
        scores: tuple[
            float,
            ...,
        ],
    ) -> SummaryTrendDirection:
        if not scores:
            return SummaryTrendDirection.UNKNOWN

        if len(
            scores,
        ) == 1:
            return SummaryTrendDirection.STABLE

        first_score = scores[0]
        latest_score = scores[-1]

        if latest_score > first_score:
            return SummaryTrendDirection.IMPROVING

        if latest_score < first_score:
            return SummaryTrendDirection.DECLINING

        return SummaryTrendDirection.STABLE