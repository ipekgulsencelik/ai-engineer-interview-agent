from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.experiment_artifact_type import (
    ExperimentArtifactType,
)
from src.evaluation.tracking.validators.experiment_artifact_validator import (
    ExperimentArtifactValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentArtifact:
    """
    Immutable experiment artifact.

    Represents an artifact produced by an
    experiment run such as reports, metrics,
    datasets, visualizations, logs, or exports.
    """

    artifact_id: str

    run_id: str

    experiment_id: str

    artifact_type: ExperimentArtifactType

    artifact_name: str

    artifact_path: str

    content_type: str

    created_at: datetime

    artifact_uri: str | None = None

    storage_backend: str | None = None

    size_bytes: int | None = None

    checksum: str | None = None

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
        ExperimentArtifactValidator.validate(
            artifact_id=self.artifact_id,
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            artifact_type=self.artifact_type,
            artifact_name=self.artifact_name,
            artifact_path=self.artifact_path,
            artifact_uri=self.artifact_uri,
            storage_backend=self.storage_backend,
            content_type=self.content_type,
            size_bytes=self.size_bytes,
            checksum=self.checksum,
            created_at=self.created_at,
            description=self.description,
            tags=self.tags,
            metadata=self.metadata,
        )

    @property
    def has_uri(
        self,
    ) -> bool:
        return (
            self.artifact_uri
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