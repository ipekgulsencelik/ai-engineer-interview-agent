from __future__ import annotations

from src.evaluation.ops.sorters.leaderboard_sorter import LeaderboardSorter
from tests.evaluation.ops.factories import experiment_snapshot


def test_leaderboard_sorter_should_sort_by_score_descending() -> None:
    snapshots = (
        experiment_snapshot(experiment_id="low", overall_score=0.70),
        experiment_snapshot(experiment_id="high", overall_score=0.95),
        experiment_snapshot(experiment_id="mid", overall_score=0.80),
    )

    sorted_snapshots = LeaderboardSorter.sort(snapshots=snapshots)

    assert tuple(
        snapshot.experiment_id for snapshot in sorted_snapshots
    ) == ("high", "mid", "low")
