from __future__ import annotations

from src.evaluation.ops.entities.dashboard_metric_card import (
    DashboardMetricCard,
)
from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class DashboardLeaderboardMetricCardsBuilder:
    """
    Builds dashboard cards from leaderboard entries.
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
                card_id="leaderboard_top_score",
                title="Leaderboard Top Score",
                value=best_entry.score,
                formatted_value=(
                    f"{best_entry.score:.2f}"
                ),
                unit=None,
                description=(
                    f"Top model: {best_entry.model_name}"
                ),
                severity=DashboardSeverity.INFO,
                sort_order=4,
            ),
        )