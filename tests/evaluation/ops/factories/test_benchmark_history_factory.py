from __future__ import annotations

from src.evaluation.ops.factories.benchmark_history_factory import BenchmarkHistoryFactory
from tests.evaluation.ops.factories import history_entry


def test_benchmark_history_factory_should_create_history() -> None:
    entry = history_entry()

    history = BenchmarkHistoryFactory.create(
        history_id="history-1",
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        entries=(entry,),
        notes="Created by factory.",
    )

    assert history.history_id == "history-1"
    assert history.entries == (entry,)
    assert history.updated_at is None
    assert history.notes == "Created by factory."
