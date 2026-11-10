"""Immutable dataset revision and derivation provenance value objects."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.evaluation.dataset.lineage.errors import DatasetLineageError
from src.evaluation.dataset.schema_evolution.models import parse_schema_version

_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class DatasetRevision:
    """Stable identity for one dataset version within a lineage graph."""

    dataset_id: str
    version: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.dataset_id, str)
            or not self.dataset_id.strip()
            or len(self.dataset_id) > 128
        ):
            raise DatasetLineageError(
                "dataset_id must be a non-empty string up to 128 characters"
            )
        parse_schema_version(self.version)


class LineageRelation(StrEnum):
    """Describes how a newly registered dataset depends on its parent."""

    DERIVED_FROM = "derived_from"
    FILTERED_FROM = "filtered_from"
    MERGED_FROM = "merged_from"
    MIGRATED_FROM = "migrated_from"


@dataclass(frozen=True, slots=True, kw_only=True)
class ParentLink:
    """An explicit, typed dependency on a previously registered revision."""

    parent: DatasetRevision
    relation: LineageRelation

    def __post_init__(self) -> None:
        if not isinstance(self.parent, DatasetRevision):
            raise DatasetLineageError("parent must be a DatasetRevision")
        if not isinstance(self.relation, LineageRelation):
            raise DatasetLineageError("relation must be a LineageRelation")


@dataclass(frozen=True, slots=True, kw_only=True)
class DatasetLineageNode:
    """Dataset provenance metadata, never the underlying sample content."""

    revision: DatasetRevision
    content_sha256: str
    producer: str
    created_at: datetime
    schema_version: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.revision, DatasetRevision):
            raise DatasetLineageError("revision must be a DatasetRevision")
        if (
            not isinstance(self.content_sha256, str)
            or _SHA256_PATTERN.fullmatch(self.content_sha256) is None
        ):
            raise DatasetLineageError(
                "content_sha256 must be a lowercase SHA-256 hex digest"
            )
        if (
            not isinstance(self.producer, str)
            or not self.producer.strip()
            or len(self.producer) > 128
        ):
            raise DatasetLineageError(
                "producer must be a non-empty string up to 128 characters"
            )
        if (
            not isinstance(self.created_at, datetime)
            or self.created_at.tzinfo is None
            or self.created_at.utcoffset() is None
        ):
            raise DatasetLineageError("created_at must be timezone-aware")
        if self.schema_version is not None:
            parse_schema_version(self.schema_version)

    @classmethod
    def from_artifact(
        cls,
        *,
        revision: DatasetRevision,
        content: bytes,
        producer: str,
        created_at: datetime,
        schema_version: str | None = None,
    ) -> DatasetLineageNode:
        """Hash exact artifact bytes; do not store the artifact itself."""
        if not isinstance(content, bytes):
            raise DatasetLineageError("content must be bytes")
        return cls(
            revision=revision,
            content_sha256=hashlib.sha256(content).hexdigest(),
            producer=producer,
            created_at=created_at,
            schema_version=schema_version,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class LineageAuditEvent:
    """Durable metadata-only registration event."""

    event_id: str
    revision: DatasetRevision
    content_sha256: str
    parent_count: int
    occurred_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class LineageRegistration:
    """Idempotent registration result; replay never creates another event."""

    created: bool
    event: LineageAuditEvent
