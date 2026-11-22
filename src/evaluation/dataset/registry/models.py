"""Immutable, content-addressed dataset catalog metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from src.evaluation.dataset.lineage.models import (
    DatasetLineageNode,
    DatasetRevision,
)
from src.evaluation.dataset.registry.errors import DatasetRegistryError
from src.evaluation.dataset.schema_evolution.models import parse_schema_version

_DIGEST = re.compile(r"[0-9a-f]{64}")
_TAG = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}")


@dataclass(frozen=True, slots=True, kw_only=True)
class DatasetCatalogEntry:
    """A single immutable revision, never source samples or artifact bytes."""

    revision: DatasetRevision
    content_sha256: str
    producer: str
    created_at: datetime
    name: str
    owner_id: str
    schema_version: str | None = None
    tags: tuple[str, ...] = ()
    description: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.revision, DatasetRevision):
            raise DatasetRegistryError("revision must be DatasetRevision")
        if (
            not isinstance(self.content_sha256, str)
            or _DIGEST.fullmatch(self.content_sha256) is None
        ):
            raise DatasetRegistryError("content_sha256 must be lowercase SHA-256")
        for field, length in (
            ("producer", 128),
            ("name", 128),
            ("owner_id", 128),
        ):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip() or len(value) > length:
                raise DatasetRegistryError(
                    f"{field} must be a non-empty string up to {length} characters"
                )
        if (
            not isinstance(self.created_at, datetime)
            or self.created_at.tzinfo is None
            or self.created_at.utcoffset() is None
        ):
            raise DatasetRegistryError("created_at must be timezone-aware")
        if self.schema_version is not None:
            parse_schema_version(self.schema_version)
        if (
            not isinstance(self.tags, tuple)
            or len(self.tags) > 32
            or any(
                not isinstance(tag, str) or _TAG.fullmatch(tag) is None
                for tag in self.tags
            )
            or len(self.tags) != len(set(self.tags))
        ):
            raise DatasetRegistryError(
                "tags must be at most 32 distinct lowercase identifiers"
            )
        # Tag order is not part of the registry's immutable logical identity.
        object.__setattr__(self, "tags", tuple(sorted(self.tags)))
        if self.description is not None and (
            not isinstance(self.description, str)
            or len(self.description) > 512
        ):
            raise DatasetRegistryError("description must be at most 512 characters")

    @classmethod
    def from_lineage(
        cls,
        *,
        node: DatasetLineageNode,
        name: str,
        owner_id: str,
        tags: tuple[str, ...] = (),
        description: str | None = None,
    ) -> DatasetCatalogEntry:
        if not isinstance(node, DatasetLineageNode):
            raise DatasetRegistryError("node must be DatasetLineageNode")
        return cls(
            revision=node.revision,
            content_sha256=node.content_sha256,
            producer=node.producer,
            created_at=node.created_at,
            schema_version=node.schema_version,
            name=name,
            owner_id=owner_id,
            tags=tags,
            description=description,
        )


@dataclass(frozen=True, slots=True)
class CatalogRegistration:
    created: bool
    entry: DatasetCatalogEntry
