from __future__ import annotations

from src.evaluation.ops.value_objects.dashboard_metric_card import (
    DashboardMetricCard,
)


class DashboardMetricCardCollectionBuilder:
    """
    Builds dashboard metric card collections.
    """

    @staticmethod
    def build(
        *,
        metric_cards: tuple[
            DashboardMetricCard,
            ...,
        ],
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        return tuple(
            sorted(
                metric_cards,
                key=lambda card: (card.sort_order,),
            ),
        )
