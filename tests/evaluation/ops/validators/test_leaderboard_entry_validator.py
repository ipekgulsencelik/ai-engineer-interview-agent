from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.leaderboard_entry_validator import (
    LeaderboardEntryValidator,
)


def _valid_kwargs() -> dict[str, object]:
    return {
        "rank": 1,
        "experiment_id": "experiment-1",
        "benchmark_id": "benchmark-1",
        "benchmark_name": "AI Engineer Benchmark",
        "benchmark_version": "1.0.0",
        "model_name": "gpt-5",
        "overall_score": 0.90,
        "dataset_id": "dataset-1",
        "dataset_version": "1.0.0",
        "dataset_hash": "sha256:abc123",
        "metrics_version": "1.0.0",
        "interpretation": "strong_benchmark",
        "tags": ("nightly",),
        "notes": "Valid entry.",
    }


def test_leaderboard_entry_validator_should_accept_valid_payload() -> None:
    LeaderboardEntryValidator.validate(**_valid_kwargs())


@pytest.mark.parametrize(
    "field_name",
    [
        "experiment_id",
        "benchmark_id",
        "benchmark_name",
        "benchmark_version",
        "model_name",
        "dataset_id",
        "dataset_version",
        "dataset_hash",
        "metrics_version",
        "interpretation",
    ],
)
def test_leaderboard_entry_validator_should_reject_empty_strings(
    field_name: str,
) -> None:
    kwargs = _valid_kwargs()
    kwargs[field_name] = ""

    with pytest.raises(EvaluationValidationError):
        LeaderboardEntryValidator.validate(**kwargs)


def test_leaderboard_entry_validator_should_reject_non_positive_rank() -> None:
    kwargs = _valid_kwargs()
    kwargs["rank"] = 0

    with pytest.raises(EvaluationValidationError):
        LeaderboardEntryValidator.validate(**kwargs)


def test_leaderboard_entry_validator_should_reject_score_outside_ratio() -> None:
    kwargs = _valid_kwargs()
    kwargs["overall_score"] = 1.1

    with pytest.raises(EvaluationValidationError):
        LeaderboardEntryValidator.validate(**kwargs)
