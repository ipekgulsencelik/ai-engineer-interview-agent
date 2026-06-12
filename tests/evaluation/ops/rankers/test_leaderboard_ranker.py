from __future__ import annotations

from src.evaluation.ops.rankers.leaderboard_ranker import LeaderboardRanker
from tests.evaluation.ops.factories import experiment_snapshot


def test_leaderboard_ranker_should_assign_one_based_ranks() -> None:
    entries = LeaderboardRanker.rank(
        snapshots=(
            experiment_snapshot(experiment_id="first", overall_score=0.90),
            experiment_snapshot(experiment_id="second", overall_score=0.80),
        ),
    )

    assert tuple(entry.rank for entry in entries) == (1, 2)
    assert tuple(entry.experiment_id for entry in entries) == ("first", "second")
