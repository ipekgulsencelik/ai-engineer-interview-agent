from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.engines.leaderboard_engine import LeaderboardEngine
from tests.evaluation.ops.factories import experiment_snapshot


def test_leaderboard_engine_should_validate_sort_and_rank_snapshots() -> None:
    entries = LeaderboardEngine().build(
        snapshots=(
            experiment_snapshot(experiment_id="low", overall_score=0.70),
            experiment_snapshot(experiment_id="high", overall_score=0.95),
        ),
    )

    assert tuple(entry.rank for entry in entries) == (1, 2)
    assert tuple(entry.experiment_id for entry in entries) == ("high", "low")


def test_leaderboard_engine_should_raise_for_empty_snapshots() -> None:
    with pytest.raises(
        EvaluationValidationError,
        match="snapshots cannot be empty",
    ):
        LeaderboardEngine().build(snapshots=())
