from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.validators.artifact_version_validator import (
    ArtifactVersionValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ArtifactVersion:
    """
    Immutable artifact version.

    Represents a versioned snapshot of an
    experiment artifact and its associated
    metadata.
    """

    version_id: str

    artifact_id: str

    version: str

    path: str

    created_at: datetime

    artifact_uri: str | None = None

    checksum: str | None = None

    size_bytes: int | None = None

    created_by: str | None = None

    change_summary: str | None = None

    parent_version_id: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ArtifactVersionValidator.validate(
            version_id=self.version_id,
            artifact_id=self.artifact_id,
            version=self.version,
            path=self.path,
            created_at=self.created_at,
            artifact_uri=self.artifact_uri,
            checksum=self.checksum,
            size_bytes=self.size_bytes,
            created_by=self.created_by,
            change_summary=self.change_summary,
            parent_version_id=self.parent_version_id,
            metadata=self.metadata,
        )

    @property
    def has_parent(
        self,
    ) -> bool:
        return (
            self.parent_version_id
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
    def has_uri(
        self,
    ) -> bool:
        return (
            self.artifact_uri
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_root_version(
        self,
    ) -> bool:
        return (
            self.parent_version_id
            is None
        )