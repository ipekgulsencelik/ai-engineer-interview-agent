from __future__ import annotations

from src.api.schemas.evaluation.leaderboard_entry_response import (
    LeaderboardEntryResponse,
)
from src.evaluation.ops.value_objects.leaderboard_entry import (
    LeaderboardEntry,
)


class LeaderboardEntryResponseMapper:
    """
    Maps leaderboard entries.
    """

    @staticmethod
    def map(
        *,
        leaderboard_entries: tuple[
            LeaderboardEntry,
            ...
        ],
    ) -> list[LeaderboardEntryResponse]:
        return [
            LeaderboardEntryResponse(
                rank=entry.rank,
                model_name=entry.model_name,
                overall_score=entry.overall_score,
            )
            for entry in leaderboard_entries
        ]