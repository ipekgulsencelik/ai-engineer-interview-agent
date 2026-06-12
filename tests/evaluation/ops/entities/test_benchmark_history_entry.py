from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)
from tests.evaluation.ops.factories import history_entry


def test_benchmark_history_entry_should_create_successfully() -> None:
    entry = history_entry(overall_score=0.82)

    assert entry.experiment_id == "experiment-1"
    assert entry.overall_score == 0.82


def test_benchmark_history_entry_should_raise_for_invalid_score() -> None:
    with pytest.raises(EvaluationValidationError, match="between 0 and 1"):
        history_entry(overall_score=1.20)


def test_benchmark_history_entry_should_raise_for_invalid_recorded_at() -> None:
    with pytest.raises(EvaluationValidationError, match="recorded_at must be datetime"):
        BenchmarkHistoryEntry(
            experiment_id="experiment-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            overall_score=0.80,
            model_name="gpt-5",
            recorded_at="now",  # type: ignore[arg-type]
        )
