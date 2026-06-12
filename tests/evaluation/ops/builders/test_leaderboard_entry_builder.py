from __future__ import annotations

from src.evaluation.ops.builders.leaderboard_entry_builder import (
    LeaderboardEntryBuilder,
)
from tests.evaluation.ops.factories import experiment_snapshot


def test_leaderboard_entry_builder_should_map_snapshot_fields() -> None:
    snapshot = experiment_snapshot(
        experiment_id="experiment-42",
        overall_score=0.91,
        tags=("candidate",),
    )

    entry = LeaderboardEntryBuilder.build(
        rank=2,
        snapshot=snapshot,
    )

    assert entry.rank == 2
    assert entry.experiment_id == "experiment-42"
    assert entry.benchmark_name == snapshot.benchmark_name
    assert entry.overall_score == 0.91
    assert entry.tags == ("candidate",)
    assert entry.notes == "snapshot notes"
