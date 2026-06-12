from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.registered_benchmark_schema import (
    REGISTERED_BENCHMARK_SCHEMA,
)


class RegisteredBenchmarkValidator:
    """
    RegisteredBenchmark validation service.
    """

    @staticmethod
    def validate(
        *,
        benchmark_id: str,
        name: str,
        version: str,
        dataset_id: str,
        dataset_version: str,
        description: str | None = None,
        owner: str | None = None,
        tags: tuple[str, ...],
        is_active: bool,
        created_at: datetime | None = None,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "benchmark_id": benchmark_id,
                "name": name,
                "version": version,
                "dataset_id": dataset_id,
                "dataset_version": dataset_version,
                "description": description,
                "owner": owner,
                "tags": tags,
                "is_active": is_active,
                "notes": notes,
            },
            schema=REGISTERED_BENCHMARK_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if created_at is not None and not isinstance(
            created_at,
            datetime,
        ):
            raise EvaluationValidationError(
                "created_at must be datetime."
            )