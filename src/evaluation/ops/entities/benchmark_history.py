from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.validators.benchmark_history_validator import (
    BenchmarkHistoryValidator,
)
from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BenchmarkHistory:
    """
    Immutable benchmark history entity.

    Stores lightweight benchmark execution history entries
    for trend analysis, leaderboard calculation, and
    regression detection.
    """

    history_id: str

    benchmark_id: str
    benchmark_version: str

    entries: tuple[
        BenchmarkHistoryEntry,
        ...,
    ]

    created_at: datetime

    updated_at: datetime | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        BenchmarkHistoryValidator.validate(
            history_id=self.history_id,
            benchmark_id=self.benchmark_id,
            benchmark_version=self.benchmark_version,
            entries=self.entries,
            created_at=self.created_at,
            updated_at=self.updated_at,
            notes=self.notes,
        )

    @property
    def entry_count(
        self,
    ) -> int:
        return len(
            self.entries,
        )

    @property
    def has_entries(
        self,
    ) -> bool:
        return bool(
            self.entries,
        )

    @property
    def latest_entry(
        self,
    ) -> BenchmarkHistoryEntry | None:
        if not self.entries:
            return None

        return max(
            self.entries,
            key=lambda entry: entry.recorded_at,
        )

    @property
    def earliest_entry(
        self,
    ) -> BenchmarkHistoryEntry | None:
        if not self.entries:
            return None

        return min(
            self.entries,
            key=lambda entry: entry.recorded_at,
        )

    @property
    def experiment_ids(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            entry.experiment_id
            for entry in self.entries
        )

    def contains_experiment(
        self,
        *,
        experiment_id: str,
    ) -> bool:
        return experiment_id in self.experiment_ids