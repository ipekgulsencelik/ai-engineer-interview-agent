from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.registered_benchmark import (
    RegisteredBenchmark,
)
from src.evaluation.ops.schemas.evaluation_registry_schema import (
    EVALUATION_REGISTRY_SCHEMA,
)


class EvaluationRegistryValidator:
    """
    EvaluationRegistry validation service.
    """

    @staticmethod
    def validate(
        *,
        registry_id: str,
        registry_name: str,
        version: str,
        benchmarks: tuple[RegisteredBenchmark, ...],
        created_at: datetime,
        updated_at: datetime | None = None,
        is_locked: bool,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "registry_id": registry_id,
                "registry_name": registry_name,
                "version": version,
                "is_locked": is_locked,
                "notes": notes,
            },
            schema=EVALUATION_REGISTRY_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        EvaluationRegistryValidator._validate_benchmarks(
            benchmarks=benchmarks,
        )

        EvaluationRegistryValidator._validate_timestamps(
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def _validate_benchmarks(
        *,
        benchmarks: tuple[RegisteredBenchmark, ...],
    ) -> None:
        if not isinstance(
            benchmarks,
            tuple,
        ):
            raise EvaluationValidationError(
                "benchmarks must be tuple."
            )

        seen_keys: set[str] = set()

        for index, benchmark in enumerate(
            benchmarks,
        ):
            if not isinstance(
                benchmark,
                RegisteredBenchmark,
            ):
                raise EvaluationValidationError(
                    f"benchmarks[{index}] must be RegisteredBenchmark."
                )

            if benchmark.identity_key in seen_keys:
                raise EvaluationValidationError(
                    "benchmarks cannot contain duplicate identity keys."
                )

            seen_keys.add(
                benchmark.identity_key,
            )

    @staticmethod
    def _validate_timestamps(
        *,
        created_at: datetime,
        updated_at: datetime | None,
    ) -> None:
        if not isinstance(
            created_at,
            datetime,
        ):
            raise EvaluationValidationError(
                "created_at must be datetime."
            )

        if updated_at is not None and not isinstance(
            updated_at,
            datetime,
        ):
            raise EvaluationValidationError(
                "updated_at must be datetime."
            )

        if (
            updated_at is not None
            and updated_at < created_at
        ):
            raise EvaluationValidationError(
                "updated_at cannot be earlier than created_at."
            )