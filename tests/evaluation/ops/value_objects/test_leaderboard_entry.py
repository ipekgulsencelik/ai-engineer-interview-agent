from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.value_objects.leaderboard_entry import LeaderboardEntry


def test_leaderboard_entry_should_create_successfully() -> None:
    entry = LeaderboardEntry(
        rank=1,
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        model_name="gpt-5",
        overall_score=0.90,
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        dataset_hash="sha256:abc123",
        metrics_version="1.0.0",
        interpretation="strong_benchmark",
        tags=("nightly",),
        notes="Top score.",
    )

    assert entry.rank == 1
    assert entry.overall_score == 0.90
    assert entry.tags == ("nightly",)


def test_leaderboard_entry_should_raise_for_invalid_rank() -> None:
    with pytest.raises(EvaluationValidationError):
        LeaderboardEntry(
            rank=0,
            experiment_id="experiment-1",
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            benchmark_version="1.0.0",
            model_name="gpt-5",
            overall_score=0.90,
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            dataset_hash="sha256:abc123",
            metrics_version="1.0.0",
            interpretation="strong_benchmark",
        )
