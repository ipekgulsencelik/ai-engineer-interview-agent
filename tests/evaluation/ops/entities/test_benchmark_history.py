from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.benchmark_history import BenchmarkHistory
from tests.evaluation.ops.factories import benchmark_history, history_entry


def test_benchmark_history_should_expose_entry_helpers() -> None:
    early = history_entry(
        experiment_id="early",
        recorded_at=datetime.now(tz=timezone.utc) - timedelta(days=1),
    )
    late = history_entry(
        experiment_id="late",
        recorded_at=datetime.now(tz=timezone.utc),
    )

    history = benchmark_history(entries=(early, late))

    assert history.entry_count == 2
    assert history.has_entries is True
    assert history.latest_entry == late
    assert history.earliest_entry == early
    assert history.experiment_ids == ("early", "late")
    assert history.contains_experiment(experiment_id="late") is True


def test_benchmark_history_should_raise_for_mismatched_entry_benchmark() -> None:
    with pytest.raises(EvaluationValidationError, match="benchmark_id does not match"):
        benchmark_history(
            entries=(
                history_entry(benchmark_id="different-benchmark"),
            ),
        )


def test_benchmark_history_should_raise_for_duplicate_experiment_ids() -> None:
    with pytest.raises(EvaluationValidationError, match="duplicate experiment_id"):
        benchmark_history(
            entries=(
                history_entry(experiment_id="same"),
                history_entry(experiment_id="same"),
            ),
        )


def test_benchmark_history_should_raise_for_invalid_updated_at_order() -> None:
    created_at = datetime.now(tz=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="earlier than created_at"):
        BenchmarkHistory(
            history_id="history-1",
            benchmark_id="benchmark-1",
            benchmark_version="1.0.0",
            entries=(),
            created_at=created_at,
            updated_at=created_at - timedelta(seconds=1),
        )
