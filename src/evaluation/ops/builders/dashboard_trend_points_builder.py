from __future__ import annotations

from src.evaluation.ops.value_objects.dashboard_trend_point import (
    DashboardTrendPoint,
)


class DashboardTrendPointsBuilder:
    """
    Builds dashboard trend points from trend snapshots.
    """

    @staticmethod
    def build(
        *,
        trend_snapshot,
    ) -> tuple[
        DashboardTrendPoint,
        ...,
    ]:
        return tuple(
            DashboardTrendPoint(
                point_id=point.point_id,
                metric_name=point.metric_name,
                value=point.value,
                occurred_at=point.occurred_at,
                unit=getattr(
                    point,
                    "unit",
                    None,
                ),
                benchmark_id=getattr(
                    point,
                    "benchmark_id",
                    None,
                ),
                experiment_id=getattr(
                    point,
                    "experiment_id",
                    None,
                ),
                model_name=getattr(
                    point,
                    "model_name",
                    None,
                ),
                label=getattr(
                    point,
                    "label",
                    None,
                ),
                notes=getattr(
                    point,
                    "notes",
                    None,
                ),
            )
            for point in getattr(
                trend_snapshot,
                "points",
                (),
            )
        )