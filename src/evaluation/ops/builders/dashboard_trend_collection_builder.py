from __future__ import annotations

from src.evaluation.ops.value_objects.dashboard_trend_point import (
    DashboardTrendPoint,
)


class DashboardTrendCollectionBuilder:
    """
    Builds dashboard trend point collections.
    """

    @staticmethod
    def build(
        *,
        trend_points: tuple[
            DashboardTrendPoint,
            ...,
        ],
    ) -> tuple[
        DashboardTrendPoint,
        ...,
    ]:
        return tuple(
            sorted(
                trend_points,
                key=lambda point: (
                    point.occurred_at,
                ),
            ),
        )