from __future__ import annotations

from src.evaluation.ops.enums.summary_trend_direction import (
    SummaryTrendDirection,
)


class SummaryTrendDirectionMapper:
    """
    Maps trend direction strings to SummaryTrendDirection.
    """

    @staticmethod
    def from_string(
        *,
        direction: str,
    ) -> SummaryTrendDirection:
        normalized_direction = direction.lower()

        if normalized_direction == "improving":
            return SummaryTrendDirection.IMPROVING

        if normalized_direction in {
            "regressing",
            "declining",
        }:
            return SummaryTrendDirection.DECLINING

        if normalized_direction == "volatile":
            return SummaryTrendDirection.VOLATILE

        if normalized_direction == "stable":
            return SummaryTrendDirection.STABLE

        return SummaryTrendDirection.UNKNOWN