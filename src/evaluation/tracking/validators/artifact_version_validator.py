from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.schemas.artifact_version_schema import (
    ARTIFACT_VERSION_SCHEMA,
)


class ArtifactVersionValidator:
    """
    ArtifactVersion validation service.
    """

    @staticmethod
    def validate(
        *,
        version_id: str,
        artifact_id: str,
        version: str,
        path: str,
        created_at: datetime,
        artifact_uri: str | None,
        checksum: str | None,
        size_bytes: int | None,
        created_by: str | None,
        change_summary: str | None,
        parent_version_id: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "version_id": version_id,
                "artifact_id": artifact_id,
                "version": version,
                "path": path,
                "created_at": created_at,
                "artifact_uri": artifact_uri,
                "checksum": checksum,
                "size_bytes": size_bytes,
                "created_by": created_by,
                "change_summary": change_summary,
                "parent_version_id": parent_version_id,
                "metadata": metadata or {},
            },
            schema=ARTIFACT_VERSION_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            parent_version_id
            is not None
            and parent_version_id == version_id
        ):
            raise EvaluationValidationError(
                "parent_version_id cannot equal version_id."
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