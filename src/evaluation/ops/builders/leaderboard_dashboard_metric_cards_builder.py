from __future__ import annotations

from src.evaluation.ops.constants.dashboard_card_descriptions import (
    TOP_MODEL_PREFIX,
)
from src.evaluation.ops.constants.dashboard_card_ids import (
    LEADERBOARD_TOP_SCORE_CARD_ID,
)
from src.evaluation.ops.constants.dashboard_card_sort_orders import (
    LEADERBOARD_SORT_ORDER,
)
from src.evaluation.ops.constants.dashboard_card_titles import (
    LEADERBOARD_TOP_SCORE_TITLE,
)
from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class LeaderboardDashboardMetricCardsBuilder:
    """
    Builds dashboard metric cards from leaderboard entries.
    """

    @staticmethod
    def build(
        *,
        leaderboard_entries,
    ) -> tuple[
        DashboardMetricCard,
        ...,
    ]:
        entries = tuple(
            leaderboard_entries,
        )

        if not entries:
            return ()

        best_entry = entries[0]

        return (
            DashboardMetricCard(
                card_id=LEADERBOARD_TOP_SCORE_CARD_ID,
                title=LEADERBOARD_TOP_SCORE_TITLE,
                value=best_entry.score,
                formatted_value=(
                    f"{best_entry.score:.2f}"
                ),
                unit=None,
                description=(
                    f"{TOP_MODEL_PREFIX} "
                    f"{best_entry.model_name}"
                ),
                severity=DashboardSeverity.INFO,
                sort_order=LEADERBOARD_SORT_ORDER,
            ),
        )