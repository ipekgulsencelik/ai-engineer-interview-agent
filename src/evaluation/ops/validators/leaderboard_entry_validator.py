from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.leaderboard_entry_schema import (
    LEADERBOARD_ENTRY_SCHEMA,
)


class LeaderboardEntryValidator:
    """
    LeaderboardEntry validation service.
    """

    @staticmethod
    def validate(
        *,
        rank: int,
        experiment_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        model_name: str,
        overall_score: float,
        dataset_id: str,
        dataset_version: str,
        dataset_hash: str,
        metrics_version: str,
        interpretation: str,
        tags: tuple[str, ...],
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "rank": rank,
                "experiment_id": experiment_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "overall_score": overall_score,
                "dataset_id": dataset_id,
                "dataset_version": dataset_version,
                "dataset_hash": dataset_hash,
                "metrics_version": metrics_version,
                "interpretation": interpretation,
                "tags": tags,
                "notes": notes,
            },
            schema=LEADERBOARD_ENTRY_SCHEMA,
            error_factory=EvaluationValidationError,
        )