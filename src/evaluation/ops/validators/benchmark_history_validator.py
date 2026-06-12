from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)
from src.evaluation.ops.schemas.benchmark_history_schema import (
    BENCHMARK_HISTORY_SCHEMA,
)


class BenchmarkHistoryValidator:
    """
    BenchmarkHistory validation service.
    """

    @staticmethod
    def validate(
        *,
        history_id: str,
        benchmark_id: str,
        benchmark_version: str,
        entries: tuple[BenchmarkHistoryEntry, ...],
        created_at: datetime,
        updated_at: datetime | None = None,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "history_id": history_id,
                "benchmark_id": benchmark_id,
                "benchmark_version": benchmark_version,
                "notes": notes,
            },
            schema=BENCHMARK_HISTORY_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        BenchmarkHistoryValidator._validate_entries(
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
            entries=entries,
        )

        BenchmarkHistoryValidator._validate_timestamps(
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def _validate_entries(
        *,
        benchmark_id: str,
        benchmark_version: str,
        entries: tuple[BenchmarkHistoryEntry, ...],
    ) -> None:
        if not isinstance(entries, tuple):
            raise EvaluationValidationError(
                "entries must be tuple."
            )

        seen_experiment_ids: set[str] = set()

        for index, entry in enumerate(entries):
            if not isinstance(entry, BenchmarkHistoryEntry):
                raise EvaluationValidationError(
                    f"entries[{index}] must be BenchmarkHistoryEntry."
                )

            if entry.benchmark_id != benchmark_id:
                raise EvaluationValidationError(
                    f"entries[{index}] benchmark_id does not match history benchmark_id."
                )

            if entry.benchmark_version != benchmark_version:
                raise EvaluationValidationError(
                    f"entries[{index}] benchmark_version does not match history benchmark_version."
                )

            if entry.experiment_id in seen_experiment_ids:
                raise EvaluationValidationError(
                    "entries cannot contain duplicate experiment_id values."
                )

            seen_experiment_ids.add(entry.experiment_id)

    @staticmethod
    def _validate_timestamps(
        *,
        created_at: datetime,
        updated_at: datetime | None,
    ) -> None:
        if not isinstance(created_at, datetime):
            raise EvaluationValidationError(
                "created_at must be datetime."
            )

        if updated_at is not None and not isinstance(updated_at, datetime):
            raise EvaluationValidationError(
                "updated_at must be datetime."
            )

        if updated_at is not None and updated_at < created_at:
            raise EvaluationValidationError(
                "updated_at cannot be earlier than created_at."
            )