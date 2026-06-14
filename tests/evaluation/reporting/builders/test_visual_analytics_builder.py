from __future__ import annotations

from src.evaluation.reporting.builders.visual_analytics_builder import VisualAnalyticsBuilder
from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection


def test_build_from_trend_creates_chart_ready_snapshot(experiment_trend) -> None:
    snapshot = VisualAnalyticsBuilder().build_from_trend(trend=experiment_trend)

    assert snapshot.title == "Experiment Trend - RAG Quality"
    assert snapshot.labels == ("run-1", "run-2")
    assert snapshot.scores == (0.7, 0.9)
    assert snapshot.average_score == 0.8
    assert snapshot.trend_direction == SummaryTrendDirection.IMPROVING
    assert snapshot.metadata == {
        "experiment_version": "v1",
        "run_count": "2",
        "first_run_id": "run-1",
        "latest_run_id": "run-2",
    }
