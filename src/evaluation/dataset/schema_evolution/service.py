"""Orchestrates safe record migrations through injected collaborators."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Protocol

from src.evaluation.dataset.schema_evolution.compatibility import (
    CompatibilityReport,
    SchemaCompatibilityChecker,
)
from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.migrations import (
    MigrationPathResolver,
)
from src.evaluation.dataset.schema_evolution.models import DatasetRecordSchema
from src.evaluation.dataset.schema_evolution.validation import (
    DatasetRecordValidator,
)


class RecordValidationPort(Protocol):
    def validate(
        self,
        *,
        schema: DatasetRecordSchema,
        record: Mapping[str, object],
    ) -> None: ...


class SchemaCompatibilityPort(Protocol):
    def compare(
        self,
        *,
        source: DatasetRecordSchema,
        target: DatasetRecordSchema,
    ) -> CompatibilityReport: ...


class SchemaEvolutionService:
    """Migrate records without mutating input or bypassing schema checks."""

    def __init__(
        self,
        *,
        migrations: MigrationPathResolver,
        validator: RecordValidationPort | None = None,
        compatibility: SchemaCompatibilityPort | None = None,
    ) -> None:
        self._migrations = migrations
        self._validator = (
            validator if validator is not None else DatasetRecordValidator()
        )
        self._compatibility = (
            compatibility if compatibility is not None
            else SchemaCompatibilityChecker()
        )

    def migrate_records(
        self,
        *,
        records: Sequence[Mapping[str, object]],
        source_schema: DatasetRecordSchema,
        target_schema: DatasetRecordSchema,
    ) -> tuple[dict[str, object], ...]:
        self._compatibility.compare(
            source=source_schema,
            target=target_schema,
        )
        path = self._migrations.resolve(
            source_version=source_schema.version,
            target_version=target_schema.version,
        )
        migrated: list[dict[str, object]] = []
        for index, record in enumerate(records):
            try:
                self._validator.validate(
                    schema=source_schema,
                    record=record,
                )
                current = deepcopy(dict(record))
                for step in path:
                    result = step.migrate(current)
                    if not isinstance(result, Mapping):
                        raise SchemaEvolutionError(
                            "migration must return a mapping"
                        )
                    current = deepcopy(dict(result))
                self._validator.validate(
                    schema=target_schema,
                    record=current,
                )
                migrated.append(current)
            except SchemaEvolutionError as exc:
                raise SchemaEvolutionError(
                    f"record[{index}]: {exc}"
                ) from exc
        return tuple(migrated)
