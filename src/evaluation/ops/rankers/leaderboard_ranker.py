from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.leaderboard_entry_builder import (
    LeaderboardEntryBuilder,
)
from src.evaluation.ops.value_objects.leaderboard_entry import (
    LeaderboardEntry,
)


class LeaderboardRanker:
    """
    Assigns ranks and creates leaderboard entries.
    """

    @staticmethod
    def rank(
        *,
        snapshots: Sequence[
            ExperimentResultSnapshot
        ],
    ) -> tuple[
        LeaderboardEntry,
        ...
    ]:
        return tuple(
            LeaderboardEntryBuilder.build(
                rank=index + 1,
                snapshot=snapshot,
            )
            for index, snapshot in enumerate(
                snapshots,
            )
        )