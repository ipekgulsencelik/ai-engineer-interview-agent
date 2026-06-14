from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.enums.model_stage import (
    ModelStage,
)
from src.evaluation.tracking.schemas.model_registry_entry_schema import (
    MODEL_REGISTRY_ENTRY_SCHEMA,
)


class ModelRegistryEntryValidator:
    """
    ModelRegistryEntry validation service.
    """

    @staticmethod
    def validate(
        *,
        registry_id: str,
        model_name: str,
        model_version: str,
        stage: ModelStage,
        created_at: datetime,
        framework: str | None,
        provider: str | None,
        model_uri: str | None,
        artifact_path: str | None,
        checksum: str | None,
        owner: str | None,
        description: str | None,
        tags: tuple[
            str,
            ...,
        ],
        metadata: dict[
            str,
            str,
        ] | None,
        benchmark_score: float | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "registry_id": registry_id,
                "model_name": model_name,
                "model_version": model_version,
                "stage": str(stage),
                "created_at": created_at,
                "framework": framework,
                "provider": provider,
                "model_uri": model_uri,
                "artifact_path": artifact_path,
                "checksum": checksum,
                "owner": owner,
                "description": description,
                "tags": tags,
                "metadata": metadata or {},
                "benchmark_score": benchmark_score,
            },
            schema=MODEL_REGISTRY_ENTRY_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            stage,
            ModelStage,
        ):
            raise EvaluationValidationError(
                "stage must be ModelStage."
            )

        for index, tag in enumerate(
            tags,
        ):
            if not isinstance(
                tag,
                str,
            ) or not tag.strip():
                raise EvaluationValidationError(
                    f"tags[{index}] must be non-empty string."
                )

        if metadata is not None:
            for key, value in metadata.items():
                if not isinstance(
                    key,
                    str,
                ) or not key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )