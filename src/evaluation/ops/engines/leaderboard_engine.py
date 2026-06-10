from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.rankers.leaderboard_ranker import (
    LeaderboardRanker,
)
from src.evaluation.ops.sorters.leaderboard_sorter import (
    LeaderboardSorter,
)
from src.evaluation.ops.validators.leaderboard_input_validator import (
    LeaderboardInputValidator,
)
from src.evaluation.ops.value_objects.leaderboard_entry import (
    LeaderboardEntry,
)


class LeaderboardEngine:
    """
    Leaderboard orchestration engine.
    """

    def build(
        self,
        *,
        snapshots: Sequence[
            ExperimentResultSnapshot
        ],
    ) -> tuple[
        LeaderboardEntry,
        ...
    ]:
        LeaderboardInputValidator.validate(
            snapshots=snapshots,
        )

        sorted_snapshots = (
            LeaderboardSorter.sort(
                snapshots=snapshots,
            )
        )

        return LeaderboardRanker.rank(
            snapshots=sorted_snapshots,
        )