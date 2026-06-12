from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.leaderboard_input_validator import (
    LeaderboardInputValidator,
)
from tests.evaluation.ops.factories import experiment_snapshot


def test_leaderboard_input_validator_should_accept_snapshots() -> None:
    LeaderboardInputValidator.validate(
        snapshots=(experiment_snapshot(),),
    )


def test_leaderboard_input_validator_should_raise_for_invalid_snapshot() -> None:
    with pytest.raises(EvaluationValidationError, match=r"snapshots\[0\]"):
        LeaderboardInputValidator.validate(
            snapshots=(object(),),  # type: ignore[arg-type]
        )
