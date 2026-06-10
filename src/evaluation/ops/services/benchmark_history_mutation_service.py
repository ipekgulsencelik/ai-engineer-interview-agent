from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)
from src.evaluation.ops.entities.benchmark_history import (
    BenchmarkHistory,
)


class BenchmarkHistoryMutationService:
    """
    Mutation service for immutable benchmark history snapshots.
    """

    @staticmethod
    def append_entry(
        *,
        history: BenchmarkHistory,
        entry: BenchmarkHistoryEntry,
    ) -> BenchmarkHistory:
        if history.contains_experiment(
            experiment_id=entry.experiment_id,
        ):
            raise EvaluationValidationError(
                "benchmark history already contains this experiment."
            )

        return replace(
            history,
            entries=(
                *history.entries,
                entry,
            ),
            updated_at=datetime.now(
                tz=timezone.utc,
            ),
        )

    @staticmethod
    def remove_entry(
        *,
        history: BenchmarkHistory,
        experiment_id: str,
    ) -> BenchmarkHistory:
        if not history.contains_experiment(
            experiment_id=experiment_id,
        ):
            raise EvaluationValidationError(
                "benchmark history entry is not found."
            )

        return replace(
            history,
            entries=tuple(
                entry
                for entry in history.entries
                if entry.experiment_id != experiment_id
            ),
            updated_at=datetime.now(
                tz=timezone.utc,
            ),
        )