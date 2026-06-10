from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.value_objects.leaderboard_entry import (
    LeaderboardEntry,
)


class LeaderboardEntryBuilder:
    """
    Builds leaderboard entries.
    """

    @staticmethod
    def build(
        *,
        rank: int,
        snapshot: ExperimentResultSnapshot,
    ) -> LeaderboardEntry:
        return LeaderboardEntry(
            rank=rank,
            experiment_id=snapshot.experiment_id,
            benchmark_id=snapshot.benchmark_id,
            benchmark_name=snapshot.benchmark_name,
            benchmark_version=(
                snapshot.benchmark_version
            ),
            model_name=snapshot.model_name,
            overall_score=(
                snapshot.overall_score
            ),
            dataset_id=snapshot.dataset_id,
            dataset_version=(
                snapshot.dataset_version
            ),
            dataset_hash=snapshot.dataset_hash,
            metrics_version=(
                snapshot.metrics_version
            ),
            interpretation=(
                snapshot.interpretation
            ),
            tags=snapshot.tags,
            notes=snapshot.notes,
        )