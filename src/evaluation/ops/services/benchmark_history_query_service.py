from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)
from src.evaluation.ops.entities.benchmark_history import (
    BenchmarkHistory,
)


class BenchmarkHistoryQueryService:
    """
    Query service for benchmark histories.
    """

    @staticmethod
    def get_entry(
        *,
        history: BenchmarkHistory,
        experiment_id: str,
    ) -> BenchmarkHistoryEntry:
        for entry in history.entries:
            if entry.experiment_id == experiment_id:
                return entry

        raise EvaluationValidationError(
            "benchmark history entry is not found."
        )

    @staticmethod
    def list_entries(
        *,
        history: BenchmarkHistory,
    ) -> tuple[BenchmarkHistoryEntry, ...]:
        return history.entries

    @staticmethod
    def list_entries_descending(
        *,
        history: BenchmarkHistory,
    ) -> tuple[BenchmarkHistoryEntry, ...]:
        return tuple(
            sorted(
                history.entries,
                key=lambda entry: entry.recorded_at,
                reverse=True,
            )
        )