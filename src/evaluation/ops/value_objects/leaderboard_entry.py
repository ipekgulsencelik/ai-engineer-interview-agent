from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.ops.validators.leaderboard_entry_validator import (
    LeaderboardEntryValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class LeaderboardEntry:
    """
    Immutable leaderboard entry.

    Represents a ranked benchmark result within
    an evaluation leaderboard.
    """

    rank: int

    experiment_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    model_name: str

    overall_score: float

    dataset_id: str
    dataset_version: str
    dataset_hash: str

    metrics_version: str

    interpretation: str

    tags: tuple[str, ...] = ()

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        LeaderboardEntryValidator.validate(
            rank=self.rank,
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            overall_score=self.overall_score,
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            dataset_hash=self.dataset_hash,
            metrics_version=self.metrics_version,
            interpretation=self.interpretation,
            tags=self.tags,
            notes=self.notes,
        )