"""Domain contracts for audited, transactional dataset migrations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True, slots=True)
class MigrationAuditEvent:
    event_id: str
    schema_name: str
    operation: str
    source_version: str
    target_version: str
    source_hash: str
    target_hash: str
    record_count: int
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class MigrationSnapshot:
    schema_name: str
    schema_version: str
    records: tuple[dict[str, object], ...]
    checksum: str


class MigrationPersistencePort(Protocol):
    """A single atomic commit of migrated records, head pointer and audit."""

    def commit_migration(
        self,
        *,
        schema_name: str,
        source_version: str,
        target_version: str,
        source_records: Sequence[Mapping[str, object]],
        target_records: Sequence[Mapping[str, object]],
    ) -> MigrationAuditEvent: ...

    def rollback_last(self, *, schema_name: str) -> MigrationAuditEvent: ...


class MigrationTelemetryPort(Protocol):
    """Best-effort reporting, decoupled from durable audit storage."""

    def publish(self, event: MigrationAuditEvent) -> None: ...
