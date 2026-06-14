from __future__ import annotations

from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection
from src.evaluation.reporting.recommenders.executive_summary_recommender import ExecutiveSummaryRecommender


def test_recommend_prioritizes_trend_and_quality_signals() -> None:
    recommender = ExecutiveSummaryRecommender()

    assert recommender.recommend(
        trend_direction=SummaryTrendDirection.IMPROVING,
        overall_score=0.85,
        pass_rate=0.9,
    ) == "promote_candidate_to_next_stage"
    assert recommender.recommend(
        trend_direction=SummaryTrendDirection.DECLINING,
        overall_score=0.9,
        pass_rate=0.9,
    ) == "pause_release_and_investigate_regression"
    assert recommender.recommend(
        trend_direction=SummaryTrendDirection.VOLATILE,
        overall_score=0.9,
        pass_rate=0.9,
    ) == "increase_sample_size_and_review_variance"
    assert recommender.recommend(
        trend_direction=SummaryTrendDirection.STABLE,
        overall_score=0.65,
        pass_rate=0.9,
    ) == "block_release_until_quality_improves"
