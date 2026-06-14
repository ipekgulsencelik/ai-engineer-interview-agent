from __future__ import annotations

from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection
from src.evaluation.reporting.mappers.experiment_trend_visual_mapper import ExperimentTrendVisualMapper


def test_mapper_extracts_scores_labels_and_direction(experiment_trend) -> None:
    mapper = ExperimentTrendVisualMapper()

    scores = mapper.scores(trend=experiment_trend)

    assert scores == (0.7, 0.9)
    assert mapper.labels(trend=experiment_trend, score_count=len(scores)) == ("run-1", "run-2")
    assert mapper.trend_direction(trend=experiment_trend) == SummaryTrendDirection.IMPROVING


def test_mapper_resolves_trend_visual_defaults(experiment_trend) -> None:
    mapper = ExperimentTrendVisualMapper()

    assert mapper.title(trend=experiment_trend) == "Experiment Trend - RAG Quality"
    assert mapper.title(trend=experiment_trend, override="Custom") == "Custom"
    assert mapper.description(trend=experiment_trend) == "Quality improved."
    assert mapper.description(trend=experiment_trend, override="Override") == "Override"
    assert mapper.metadata(
        trend=experiment_trend,
        extra_metadata={"owner": "qa"},
    ) == {
        "owner": "qa",
        "experiment_version": "v1",
        "first_run_id": "run-1",
        "latest_run_id": "run-2",
        "run_count": "2",
    }
