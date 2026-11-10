"""Application boundary for persistent, observable record migrations."""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from typing import Protocol

from src.evaluation.dataset.schema_evolution.models import DatasetRecordSchema
from src.evaluation.dataset.schema_evolution.persistence import (
    MigrationAuditEvent,
    MigrationPersistencePort,
    MigrationTelemetryPort,
)


class RecordMigrationPort(Protocol):
    def migrate_records(
        self,
        *,
        records: Sequence[Mapping[str, object]],
        source_schema: DatasetRecordSchema,
        target_schema: DatasetRecordSchema,
    ) -> tuple[dict[str, object], ...]: ...


class DatasetMigrationCoordinator:
    """Only commit a fully validated batch; emit best-effort telemetry."""

    def __init__(
        self,
        *,
        migrator: RecordMigrationPort,
        persistence: MigrationPersistencePort,
        telemetry: MigrationTelemetryPort | None = None,
    ) -> None:
        self._migrator = migrator
        self._persistence = persistence
        self._telemetry = telemetry

    def execute(
        self,
        *,
        records: Sequence[Mapping[str, object]],
        source_schema: DatasetRecordSchema,
        target_schema: DatasetRecordSchema,
    ) -> MigrationAuditEvent:
        migrated = self._migrator.migrate_records(
            records=records,
            source_schema=source_schema,
            target_schema=target_schema,
        )
        event = self._persistence.commit_migration(
            schema_name=source_schema.name,
            source_version=source_schema.version,
            target_version=target_schema.version,
            source_records=records,
            target_records=migrated,
        )
        self._notify(event)
        return event

    def rollback_last(self, *, schema_name: str) -> MigrationAuditEvent:
        event = self._persistence.rollback_last(schema_name=schema_name)
        self._notify(event)
        return event

    def _notify(self, event: MigrationAuditEvent) -> None:
        if self._telemetry is None:
            return
        try:
            self._telemetry.publish(event)
        except Exception:
            # Observability must not turn an already committed migration
            # into an apparent failure or invite an unsafe retry.
            logging.getLogger(__name__).exception(
                "Migration telemetry delivery failed; committed audit is intact"
            )
