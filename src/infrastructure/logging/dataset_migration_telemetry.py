"""Structured metadata-only telemetry adapter for durable migration events."""

from __future__ import annotations

import logging

from src.evaluation.dataset.schema_evolution.persistence import (
    MigrationAuditEvent,
)


class LoggingDatasetMigrationTelemetry:
    """Log stable audit identifiers and metrics, never record content."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = (
            logger if logger is not None
            else logging.getLogger("dataset.schema_evolution")
        )

    def publish(self, event: MigrationAuditEvent) -> None:
        self._logger.info(
            "dataset migration %s: %s %s -> %s (%d records)",
            event.event_id,
            event.operation,
            event.source_version,
            event.target_version,
            event.record_count,
            extra={
                "migration_event_id": event.event_id,
                "migration_schema_name": event.schema_name,
                "migration_operation": event.operation,
                "migration_source_version": event.source_version,
                "migration_target_version": event.target_version,
                "migration_record_count": event.record_count,
                "migration_source_hash": event.source_hash,
                "migration_target_hash": event.target_hash,
            },
        )
