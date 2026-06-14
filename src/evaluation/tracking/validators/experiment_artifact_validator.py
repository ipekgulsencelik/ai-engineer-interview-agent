from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.enums.experiment_artifact_type import (
    ExperimentArtifactType,
)
from src.evaluation.tracking.schemas.experiment_artifact_schema import (
    EXPERIMENT_ARTIFACT_SCHEMA,
)


class ExperimentArtifactValidator:
    """
    ExperimentArtifact validation service.
    """

    @staticmethod
    def validate(
        *,
        artifact_id: str,
        run_id: str,
        experiment_id: str,
        artifact_type: ExperimentArtifactType,
        artifact_name: str,
        artifact_path: str,
        artifact_uri: str | None,
        storage_backend: str | None,
        content_type: str,
        size_bytes: int | None,
        checksum: str | None,
        created_at: datetime,
        description: str | None,
        tags: tuple[
            str,
            ...,
        ],
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "artifact_id": artifact_id,
                "run_id": run_id,
                "experiment_id": experiment_id,
                "artifact_type": str(
                    artifact_type,
                ),
                "artifact_name": artifact_name,
                "artifact_path": artifact_path,
                "artifact_uri": artifact_uri,
                "storage_backend": storage_backend,
                "content_type": content_type,
                "size_bytes": size_bytes,
                "checksum": checksum,
                "created_at": created_at,
                "description": description,
                "tags": tags,
                "metadata": (
                    metadata
                    or {}
                ),
            },
            schema=EXPERIMENT_ARTIFACT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            artifact_type,
            ExperimentArtifactType,
        ):
            raise EvaluationValidationError(
                "artifact_type must be ExperimentArtifactType."
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