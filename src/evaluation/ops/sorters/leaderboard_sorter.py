from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)


class LeaderboardSorter:
    """
    Sorts experiment snapshots by score.
    """

    @staticmethod
    def sort(
        *,
        snapshots: Sequence[
            ExperimentResultSnapshot
        ],
    ) -> tuple[
        ExperimentResultSnapshot,
        ...
    ]:
        return tuple(
            sorted(
                snapshots,
                key=lambda snapshot: (
                    snapshot.overall_score
                ),
                reverse=True,
            )
        )