from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.services.benchmark_history_query_service import (
    BenchmarkHistoryQueryService,
)
from tests.evaluation.ops.factories import benchmark_history, history_entry


def test_benchmark_history_query_service_should_get_and_list_entries() -> None:
    first = history_entry(
        experiment_id="first",
        recorded_at=datetime.now(tz=timezone.utc) - timedelta(days=1),
    )
    second = history_entry(
        experiment_id="second",
        recorded_at=datetime.now(tz=timezone.utc),
    )
    history = benchmark_history(entries=(first, second))

    assert BenchmarkHistoryQueryService.get_entry(
        history=history,
        experiment_id="first",
    ) == first
    assert BenchmarkHistoryQueryService.list_entries(history=history) == (
        first,
        second,
    )
    assert BenchmarkHistoryQueryService.list_entries_descending(
        history=history,
    ) == (second, first)


def test_benchmark_history_query_service_should_raise_for_missing_entry() -> None:
    with pytest.raises(EvaluationValidationError, match="entry is not found"):
        BenchmarkHistoryQueryService.get_entry(
            history=benchmark_history(),
            experiment_id="missing",
        )
