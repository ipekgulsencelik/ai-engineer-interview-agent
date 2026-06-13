from __future__ import annotations

from src.evaluation.ops.builders.aggregate_dashboard_metric_cards_builder import (
    AggregateDashboardMetricCardsBuilder,
)
from src.evaluation.ops.builders.ci_policy_dashboard_metric_cards_builder import (
    CIPolicyDashboardMetricCardsBuilder,
)
from src.evaluation.ops.builders.leaderboard_dashboard_metric_cards_builder import (
    LeaderboardDashboardMetricCardsBuilder,
)
from src.evaluation.ops.builders.regression_dashboard_metric_cards_builder import (
    RegressionDashboardMetricCardsBuilder,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)


class DashboardMetricCardsComposer:
    """
    Composes all dashboard metric cards.
    """

    def __init__(
        self,
        *,
        aggregate_cards_builder: (
            AggregateDashboardMetricCardsBuilder | None
        ) = None,
        regression_cards_builder: (
            RegressionDashboardMetricCardsBuilder | None
        ) = None,
        ci_policy_cards_builder: (
            CIPolicyDashboardMetricCardsBuilder | None
        ) = None,
        leaderboard_cards_builder: (
            LeaderboardDashboardMetricCardsBuilder | None
        ) = None,
    ) -> None:
        self._aggregate_cards_builder = (
            aggregate_cards_builder
            or AggregateDashboardMetricCardsBuilder()
        )

        self._regression_cards_builder = (
            regression_cards_builder
            or RegressionDashboardMetricCardsBuilder()
        )

        self._ci_policy_cards_builder = (
            ci_policy_cards_builder
            or CIPolicyDashboardMetricCardsBuilder()
        )

        self._leaderboard_cards_builder = (
            leaderboard_cards_builder
            or LeaderboardDashboardMetricCardsBuilder()
        )

    def compose(
        self,
        *,
        aggregate_result,
        regression_result,
        ci_policy_result,
        leaderboard_entries,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        cards = (
            self._aggregate_cards_builder.build(
                aggregate_result=aggregate_result,
            )
            + self._regression_cards_builder.build(
                regression_result=regression_result,
            )
            + self._ci_policy_cards_builder.build(
                ci_policy_result=ci_policy_result,
            )
            + self._leaderboard_cards_builder.build(
                leaderboard_entries=leaderboard_entries,
            )
        )

        return tuple(
            sorted(
                cards,
                key=lambda card: (
                    card.sort_order
                ),
            )
        )