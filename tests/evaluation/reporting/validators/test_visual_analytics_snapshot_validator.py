from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import EvaluationValidationError
from src.evaluation.reporting.validators.visual_analytics_snapshot_validator import VisualAnalyticsSnapshotValidator


def test_validate_accepts_valid_snapshot_payload(visual_snapshot) -> None:
    VisualAnalyticsSnapshotValidator.validate(
        snapshot_id=visual_snapshot.snapshot_id,
        title=visual_snapshot.title,
        chart_type=visual_snapshot.chart_type,
        created_at=visual_snapshot.created_at,
        labels=visual_snapshot.labels,
        scores=visual_snapshot.scores,
        average_score=visual_snapshot.average_score,
        trend_direction=visual_snapshot.trend_direction,
        x_axis_label=visual_snapshot.x_axis_label,
        y_axis_label=visual_snapshot.y_axis_label,
        series_name=visual_snapshot.series_name,
        experiment_id=visual_snapshot.experiment_id,
        run_id=visual_snapshot.run_id,
        benchmark_id=visual_snapshot.benchmark_id,
        model_name=visual_snapshot.model_name,
        description=visual_snapshot.description,
        metadata=visual_snapshot.metadata,
    )


def test_validate_rejects_invalid_metadata_type(visual_snapshot) -> None:
    with pytest.raises(EvaluationValidationError):
        VisualAnalyticsSnapshotValidator.validate(
            snapshot_id=visual_snapshot.snapshot_id,
            title=visual_snapshot.title,
            chart_type=visual_snapshot.chart_type,
            created_at=visual_snapshot.created_at,
            labels=visual_snapshot.labels,
            scores=visual_snapshot.scores,
            average_score=visual_snapshot.average_score,
            trend_direction=visual_snapshot.trend_direction,
            x_axis_label=visual_snapshot.x_axis_label,
            y_axis_label=visual_snapshot.y_axis_label,
            series_name=visual_snapshot.series_name,
            experiment_id=visual_snapshot.experiment_id,
            run_id=visual_snapshot.run_id,
            benchmark_id=visual_snapshot.benchmark_id,
            model_name=visual_snapshot.model_name,
            description=visual_snapshot.description,
            metadata="invalid",
        )
