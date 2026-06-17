from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.experiment_artifact_type import (
    ExperimentArtifactType,
)
from src.evaluation.reporting.validators.report_artifact_validator import (
    ReportArtifactValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReportArtifact:
    """
    Immutable report artifact.

    Represents a generated report file produced by
    evaluation operations such as executive summaries,
    experiment comparisons, trend reports, dashboards,
    benchmark reports, and CI quality gate reports.
    """

    report_id: str

    artifact_id: str

    run_id: str

    experiment_id: str

    title: str

    report_type: str

    artifact_type: ExperimentArtifactType

    path: str

    content_type: str

    created_at: datetime

    content: str | None = None

    uri: str | None = None

    storage_backend: str | None = None

    format: str | None = None

    size_bytes: int | None = None

    checksum: str | None = None

    generated_by: str | None = None

    description: str | None = None

    tags: tuple[
        str,
        ...,
    ] = ()

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ReportArtifactValidator.validate(
            report_id=self.report_id,
            artifact_id=self.artifact_id,
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            title=self.title,
            report_type=self.report_type,
            artifact_type=self.artifact_type,
            path=self.path,
            content=self.content,
            uri=self.uri,
            storage_backend=self.storage_backend,
            format=self.format,
            content_type=self.content_type,
            size_bytes=self.size_bytes,
            checksum=self.checksum,
            generated_by=self.generated_by,
            created_at=self.created_at,
            description=self.description,
            tags=self.tags,
            metadata=self.metadata,
        )

    @property
    def has_content(
        self,
    ) -> bool:
        return (
            self.content
            is not None
        )

    @property
    def has_uri(
        self,
    ) -> bool:
        return (
            self.uri
            is not None
        )

    @property
    def has_storage_backend(
        self,
    ) -> bool:
        return (
            self.storage_backend
            is not None
        )

    @property
    def has_format(
        self,
    ) -> bool:
        return (
            self.format
            is not None
        )

    @property
    def has_checksum(
        self,
    ) -> bool:
        return (
            self.checksum
            is not None
        )

    @property
    def has_generated_by(
        self,
    ) -> bool:
        return (
            self.generated_by
            is not None
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_tags(
        self,
    ) -> bool:
        return bool(
            self.tags,
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return (
            self.size_bytes == 0
        )

    @property
    def content_length(
        self,
    ) -> int:
        if self.content is None:
            return 0

        return len(
            self.content,
        )

    @property
    def is_markdown(
        self,
    ) -> bool:
        return (
            self.format == "markdown"
        )

    @property
    def is_html(
        self,
    ) -> bool:
        return (
            self.format == "html"
        )

    @property
    def is_json(
        self,
    ) -> bool:
        return (
            self.format == "json"
        )

    @property
    def is_pdf(
        self,
    ) -> bool:
        return (
            self.format == "pdf"
        )