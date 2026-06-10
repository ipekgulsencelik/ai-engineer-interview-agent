from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)
from src.evaluation.ops.entities.benchmark_history import (
    BenchmarkHistory,
)


class BenchmarkHistoryFactory:
    """
    Creates immutable benchmark history snapshots.
    """

    @staticmethod
    def create(
        *,
        history_id: str,
        benchmark_id: str,
        benchmark_version: str,
        entries: tuple[BenchmarkHistoryEntry, ...] = (),
        notes: str | None = None,
    ) -> BenchmarkHistory:
        return BenchmarkHistory(
            history_id=history_id,
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
            entries=entries,
            created_at=datetime.now(
                tz=timezone.utc,
            ),
            updated_at=None,
            notes=notes,
        )