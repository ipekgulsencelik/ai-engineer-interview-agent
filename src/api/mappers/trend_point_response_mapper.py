from __future__ import annotations

from src.evaluation.metrics.value_objects.trend_visualization_snapshot import (
    TrendVisualizationSnapshot,
)
from src.api.schemas.evaluation.trend_point_response import (
    TrendPointResponse,
)


class TrendPointResponseMapper:
    """
    Maps trend visualization points.
    """

    @staticmethod
    def map(
        *,
        trend_snapshot: TrendVisualizationSnapshot,
    ) -> list[TrendPointResponse]:
        return [
            TrendPointResponse(
                label=label,
                score=score,
            )
            for label, score
            in trend_snapshot.data_points
        ]