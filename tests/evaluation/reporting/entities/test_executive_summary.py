from __future__ import annotations

from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection


def test_executive_summary_exposes_state_properties(executive_summary) -> None:
    assert executive_summary.has_findings is True
    assert executive_summary.has_strengths is True
    assert executive_summary.has_weaknesses is True
    assert executive_summary.has_recommendations is True
    assert executive_summary.has_score is True
    assert executive_summary.has_pass_rate is True
    assert executive_summary.has_run_metrics is True
    assert executive_summary.has_average_score is True
    assert executive_summary.has_best_score is True
    assert executive_summary.has_risk_level is True
    assert executive_summary.has_confidence_level is True
    assert executive_summary.has_trend_direction is True
    assert executive_summary.has_recommendation is True
    assert executive_summary.trend_direction == SummaryTrendDirection.IMPROVING
    assert executive_summary.is_improving is True
