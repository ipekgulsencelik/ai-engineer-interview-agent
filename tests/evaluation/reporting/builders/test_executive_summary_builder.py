from __future__ import annotations

from src.evaluation.reporting.builders.executive_summary_builder import ExecutiveSummaryBuilder
from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection


def test_build_from_metrics_composes_assessment_and_recommendation() -> None:
    summary = ExecutiveSummaryBuilder().build_from_metrics(
        title="Release Gate",
        overall_score=0.86,
        pass_rate=0.91,
        total_runs=4,
        average_score=0.82,
        best_score=0.9,
        trend_direction=SummaryTrendDirection.IMPROVING,
        key_findings=("Quality improved",),
    )

    assert summary.title == "Release Gate"
    assert summary.overall_assessment == "strong"
    assert summary.recommendation == "promote_candidate_to_next_stage"
    assert summary.has_findings is True
