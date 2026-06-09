from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.detectors.benchmark_trend_detector import (
    BenchmarkTrendDetector,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.mappers.experiment_snapshot_trend_data_point_mapper import (
    ExperimentSnapshotTrendDataPointMapper,
)
from src.evaluation.metrics.validators.trend_visualization_input_validator import (
    TrendVisualizationInputValidator,
)
from src.evaluation.metrics.value_objects.trend_visualization_snapshot import (
    TrendVisualizationSnapshot,
)


class TrendVisualizationBuilder:
    """
    Builds chart-ready benchmark trend visualization snapshots.
    """

    def __init__(
        self,
        *,
        trend_detector: BenchmarkTrendDetector | None = None,
        data_point_mapper: (
            ExperimentSnapshotTrendDataPointMapper | None
        ) = None,
    ) -> None:
        self._trend_detector = (
            trend_detector
            or BenchmarkTrendDetector()
        )

        self._data_point_mapper = (
            data_point_mapper
            or ExperimentSnapshotTrendDataPointMapper()
        )

    def build_from_experiment_snapshots(
        self,
        *,
        title: str,
        description: str,
        snapshots: Sequence[ExperimentResultSnapshot],
        notes: str | None = None,
    ) -> TrendVisualizationSnapshot:
        TrendVisualizationInputValidator.validate(
            snapshots=snapshots,
        )

        data_points = tuple(
            self._data_point_mapper.map(
                snapshot=snapshot,
            )
            for snapshot in snapshots
        )

        scores = tuple(
            data_point.value
            for data_point in data_points
        )

        trend_direction = self._trend_detector.detect(
            scores=scores,
        )

        return TrendVisualizationSnapshot(
            title=title,
            description=description,
            trend_direction=trend_direction,
            data_points=data_points,
            notes=notes,
        )