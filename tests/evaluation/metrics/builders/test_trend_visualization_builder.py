from __future__ import annotations

import pytest

from src.evaluation.metrics.builders.trend_visualization_builder import (
    TrendVisualizationBuilder,
)
from src.evaluation.metrics.value_objects.trend_visualization_snapshot import (
    TrendVisualizationSnapshot,
)
from tests.evaluation.metrics.builders.test_benchmark_aggregate_result_builder import (
    _snapshot,
)


def test_trend_visualization_builder_should_build_snapshot_from_experiments() -> None:
    visualization = TrendVisualizationBuilder().build_from_experiment_snapshots(
        title="Benchmark trend",
        description="Benchmark score movement across experiments.",
        snapshots=(
            _snapshot(
                experiment_id="experiment-1",
                score=0.70,
            ),
            _snapshot(
                experiment_id="experiment-2",
                score=0.80,
            ),
            _snapshot(
                experiment_id="experiment-3",
                score=0.90,
            ),
        ),
        notes="Trend visualization builder test.",
    )

    assert isinstance(visualization, TrendVisualizationSnapshot)
    assert visualization.title == "Benchmark trend"
    assert visualization.description == "Benchmark score movement across experiments."
    assert visualization.trend_direction == "improving"
    assert visualization.point_count == 3
    assert tuple(point.label for point in visualization.data_points) == (
        "experiment-1",
        "experiment-2",
        "experiment-3",
    )
    assert tuple(point.value for point in visualization.data_points) == (
        0.70,
        0.80,
        0.90,
    )
    assert visualization.delta == pytest.approx(0.20)
    assert visualization.has_positive_trend is True
    assert visualization.notes == "Trend visualization builder test."
