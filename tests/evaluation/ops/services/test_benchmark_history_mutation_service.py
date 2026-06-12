from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.services.benchmark_history_mutation_service import (
    BenchmarkHistoryMutationService,
)
from tests.evaluation.ops.factories import benchmark_history, history_entry


def test_benchmark_history_mutation_service_should_append_entry() -> None:
    entry = history_entry()
    history = benchmark_history()

    updated = BenchmarkHistoryMutationService.append_entry(
        history=history,
        entry=entry,
    )

    assert updated.entries == (entry,)
    assert updated.updated_at is not None
    assert history.entries == ()


def test_benchmark_history_mutation_service_should_reject_duplicate_entry() -> None:
    entry = history_entry()
    history = benchmark_history(entries=(entry,))

    with pytest.raises(EvaluationValidationError, match="already contains"):
        BenchmarkHistoryMutationService.append_entry(
            history=history,
            entry=entry,
        )


def test_benchmark_history_mutation_service_should_remove_entry() -> None:
    entry = history_entry()
    history = benchmark_history(entries=(entry,))

    updated = BenchmarkHistoryMutationService.remove_entry(
        history=history,
        experiment_id="experiment-1",
    )

    assert updated.entries == ()


def test_benchmark_history_mutation_service_should_raise_for_missing_entry() -> None:
    with pytest.raises(EvaluationValidationError, match="entry is not found"):
        BenchmarkHistoryMutationService.remove_entry(
            history=benchmark_history(),
            experiment_id="missing",
        )
