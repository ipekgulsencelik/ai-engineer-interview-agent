from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.value_objects.trend_data_point import (
    TrendDataPoint,
)


class ExperimentSnapshotTrendDataPointMapper:
    """
    Maps ExperimentResultSnapshot into TrendDataPoint.
    """

    @staticmethod
    def map(
        *,
        snapshot: ExperimentResultSnapshot,
    ) -> TrendDataPoint:
        return TrendDataPoint(
            label=snapshot.experiment_id,
            value=snapshot.overall_score,
        )