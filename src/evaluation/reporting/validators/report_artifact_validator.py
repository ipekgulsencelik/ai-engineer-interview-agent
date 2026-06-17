from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.enums.experiment_artifact_type import (
    ExperimentArtifactType,
)
from src.evaluation.reporting.schemas.report_artifact_schema import (
    REPORT_ARTIFACT_SCHEMA,
)


class ReportArtifactValidator:
    """
    ReportArtifact validation service.
    """

    @staticmethod
    def validate(
        *,
        report_id: str,
        artifact_id: str,
        run_id: str,
        experiment_id: str,
        title: str,
        report_type: str,
        artifact_type: ExperimentArtifactType,
        path: str,
        content: str | None,
        uri: str | None,
        storage_backend: str | None,
        format: str | None,
        content_type: str,
        size_bytes: int | None,
        checksum: str | None,
        generated_by: str | None,
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
                "report_id": report_id,
                "artifact_id": artifact_id,
                "run_id": run_id,
                "experiment_id": experiment_id,
                "title": title,
                "report_type": report_type,
                "artifact_type": str(
                    artifact_type,
                ),
                "path": path,
                "content": content,
                "uri": uri,
                "storage_backend": storage_backend,
                "format": format,
                "content_type": content_type,
                "size_bytes": (
                    0
                    if size_bytes is None
                    else size_bytes
                ),
                "checksum": checksum,
                "generated_by": generated_by,
                "created_at": created_at,
                "description": description,
                "tags": tags,
                "metadata": metadata or {},
            },
            schema=REPORT_ARTIFACT_SCHEMA,
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

        if (
            format is not None
            and format
            not in {
                "markdown",
                "html",
                "json",
                "pdf",
                "txt",
            }
        ):
            raise EvaluationValidationError(
                "format must be one of: markdown, html, json, pdf, txt."
            )

        if (
            content is not None
            and content_type == "application/pdf"
        ):
            raise EvaluationValidationError(
                "content should not be stored inline for PDF reports."
            )