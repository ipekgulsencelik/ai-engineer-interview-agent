from __future__ import annotations

import pytest

from src.evaluation.metrics.mappers.experiment_snapshot_trend_data_point_mapper import (
    ExperimentSnapshotTrendDataPointMapper,
)
from src.evaluation.metrics.value_objects.trend_data_point import TrendDataPoint
from tests.evaluation.metrics.calculators.test_benchmark_aggregate_statistics_calculator import (
    _snapshot,
)


def test_experiment_snapshot_trend_data_point_mapper_should_map_id_and_score() -> None:
    snapshot = _snapshot(
        experiment_id="experiment-42",
        score=0.87,
    )

    data_point = ExperimentSnapshotTrendDataPointMapper.map(
        snapshot=snapshot,
    )

    assert isinstance(data_point, TrendDataPoint)
    assert data_point.label == "experiment-42"
    assert data_point.value == pytest.approx(0.87)
