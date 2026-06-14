from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.evaluation.reporting.entities.executive_summary import ExecutiveSummary
from src.evaluation.reporting.entities.visual_analytics_snapshot import VisualAnalyticsSnapshot
from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection
from src.evaluation.tracking.entities.experiment_comparison_result import ExperimentComparisonResult
from src.evaluation.tracking.entities.experiment_trend_result import ExperimentTrendResult
from src.evaluation.tracking.enums.experiment_trend_direction import ExperimentTrendDirection


@pytest.fixture
def executive_summary() -> ExecutiveSummary:
    return ExecutiveSummary(
        summary_id="summary-1",
        title="Weekly Evaluation",
        overall_assessment="strong",
        key_findings=("Accuracy improved",),
        strengths=("Stable retrieval",),
        weaknesses=("Latency variance",),
        recommendations=("Monitor latency",),
        overall_score=0.86,
        pass_rate=0.9,
        total_runs=5,
        average_score=0.84,
        best_score=0.91,
        risk_level="low",
        trend_direction=SummaryTrendDirection.IMPROVING,
        confidence_level=0.95,
        recommendation="promote_candidate_to_next_stage",
        generated_by="evaluation-ci",
        notes="Ready for review.",
    )


@pytest.fixture
def visual_snapshot() -> VisualAnalyticsSnapshot:
    return VisualAnalyticsSnapshot(
        snapshot_id="snapshot-1",
        title="Trend",
        chart_type="line",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        labels=("run-1", "run-2"),
        scores=(0.7, 0.9),
        average_score=0.8,
        trend_direction=SummaryTrendDirection.IMPROVING,
        description="Improving trend",
        metadata={"experiment_version": "v1"},
    )


@pytest.fixture
def experiment_trend() -> ExperimentTrendResult:
    return ExperimentTrendResult(
        experiment_id="exp-1",
        experiment_name="RAG Quality",
        experiment_version="v1",
        run_count=2,
        first_run_id="run-1",
        latest_run_id="run-2",
        first_overall_score=0.7,
        latest_overall_score=0.9,
        average_overall_score=0.8,
        overall_score_delta=0.2,
        first_pass_rate=0.75,
        latest_pass_rate=0.95,
        pass_rate_delta=0.2,
        best_run_id="run-2",
        best_overall_score=0.9,
        worst_run_id="run-1",
        worst_overall_score=0.7,
        trend_direction=ExperimentTrendDirection.IMPROVING,
        interpretation="Quality improved.",
        notes="No regressions.",
    )


@pytest.fixture
def experiment_comparison() -> ExperimentComparisonResult:
    return ExperimentComparisonResult(
        baseline_run_id="base-run",
        candidate_run_id="candidate-run",
        baseline_experiment_id="base-exp",
        candidate_experiment_id="candidate-exp",
        baseline_experiment_name="Baseline",
        candidate_experiment_name="Candidate",
        baseline_experiment_version="v1",
        candidate_experiment_version="v2",
        baseline_overall_score=0.75,
        candidate_overall_score=0.88,
        overall_score_delta=0.13,
        baseline_pass_rate=0.7,
        candidate_pass_rate=0.9,
        pass_rate_delta=0.2,
        baseline_sample_count=10,
        candidate_sample_count=12,
        sample_count_delta=2,
        winner_experiment_id="candidate-exp",
        interpretation="Candidate is better.",
        notes="Promote candidate.",
    )
