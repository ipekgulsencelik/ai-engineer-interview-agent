from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.validators.benchmark_history_validator import (
    BenchmarkHistoryValidator,
)
from src.evaluation.ops.validators.evaluation_registry_validator import (
    EvaluationRegistryValidator,
)
from src.evaluation.ops.validators.leaderboard_entry_validator import (
    LeaderboardEntryValidator,
)
from src.evaluation.ops.validators.registered_benchmark_validator import (
    RegisteredBenchmarkValidator,
)
from tests.evaluation.ops.factories import history_entry, registered_benchmark


def test_registered_benchmark_validator_should_raise_for_invalid_tags() -> None:
    with pytest.raises(EvaluationValidationError):
        RegisteredBenchmarkValidator.validate(
            benchmark_id="benchmark-1",
            name="AI Engineer Benchmark",
            version="1.0.0",
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            tags=(1,),  # type: ignore[arg-type]
            is_active=True,
        )


def test_evaluation_registry_validator_should_raise_for_invalid_benchmarks_type() -> None:
    with pytest.raises(EvaluationValidationError, match="benchmarks must be tuple"):
        EvaluationRegistryValidator._validate_benchmarks(
            benchmarks=[registered_benchmark()],  # type: ignore[arg-type]
        )


def test_benchmark_history_validator_should_raise_for_invalid_entries_type() -> None:
    with pytest.raises(EvaluationValidationError, match="entries must be tuple"):
        BenchmarkHistoryValidator._validate_entries(
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            entries=[history_entry()],  # type: ignore[arg-type]
        )


def test_leaderboard_entry_validator_should_raise_for_invalid_score() -> None:
    with pytest.raises(EvaluationValidationError):
        LeaderboardEntryValidator.validate(
            rank=1,
            experiment_id="experiment-1",
            benchmark_id="benchmark-1",
            benchmark_name="AI Engineer Benchmark",
            benchmark_version="1.0.0",
            model_name="gpt-5",
            overall_score=1.2,
            dataset_id="dataset-1",
            dataset_version="1.0.0",
            dataset_hash="sha256:abc123",
            metrics_version="1.0.0",
            interpretation="strong_benchmark",
            tags=(),
        )
