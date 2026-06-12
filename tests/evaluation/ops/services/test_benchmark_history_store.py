from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.services.benchmark_history_store import BenchmarkHistoryStore
from tests.evaluation.ops.factories import benchmark_history


def test_benchmark_history_store_should_save_get_list_delete_and_clear() -> None:
    store = BenchmarkHistoryStore()
    history = benchmark_history()

    store.save(history=history)

    assert store.contains(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
    ) is True
    assert store.get(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
    ) == history
    assert store.list_all() == (history,)

    store.delete(
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
    )
    assert store.list_all() == ()

    store.save(history=history)
    store.clear()
    assert store.list_all() == ()


def test_benchmark_history_store_should_raise_for_missing_history() -> None:
    store = BenchmarkHistoryStore()

    with pytest.raises(EvaluationValidationError, match="history is not found"):
        store.get(
            benchmark_id="missing",
            benchmark_version="1.0.0",
        )

    with pytest.raises(EvaluationValidationError, match="history is not found"):
        store.delete(
            benchmark_id="missing",
            benchmark_version="1.0.0",
        )
