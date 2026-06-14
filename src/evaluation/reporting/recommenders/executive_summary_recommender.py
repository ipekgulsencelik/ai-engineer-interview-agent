from __future__ import annotations

from src.evaluation.reporting.enums.summary_trend_direction import (
    SummaryTrendDirection,
)


class ExecutiveSummaryRecommender:
    """
    Builds executive recommendations from trend
    and KPI signals.
    """

    @staticmethod
    def recommend(
        *,
        trend_direction: SummaryTrendDirection,
        overall_score: float,
        pass_rate: float,
    ) -> str:
        if (
            trend_direction
            == SummaryTrendDirection.IMPROVING
            and overall_score >= 0.80
            and pass_rate >= 0.80
        ):
            return "promote_candidate_to_next_stage"

        if (
            trend_direction
            == SummaryTrendDirection.DECLINING
        ):
            return "pause_release_and_investigate_regression"

        if (
            trend_direction
            == SummaryTrendDirection.VOLATILE
        ):
            return "increase_sample_size_and_review_variance"

        if overall_score < 0.70:
            return "block_release_until_quality_improves"

        return "continue_monitoring"