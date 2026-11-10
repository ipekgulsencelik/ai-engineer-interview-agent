"""Orchestrates validated record migrations through injected collaborators."""

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


class SchemaLookupPort(Protocol):
    def get_schema(
        self, *, name: str, version: str
    ) -> DatasetRecordSchema: ...


class SchemaEvolutionService:
    """Migrate records without modifying inputs or bypassing schema checks."""

    def __init__(
        self,
        *,
        migrations: MigrationPathResolver,
        validator: RecordValidationPort | None = None,
        compatibility: SchemaCompatibilityPort | None = None,
        intermediate_schemas: SchemaLookupPort | None = None,
    ) -> None:
        self._migrations = migrations
        self._validator = (
            validator if validator is not None else DatasetRecordValidator()
        )
        self._compatibility = (
            compatibility if compatibility is not None
            else SchemaCompatibilityChecker()
        )
        self._intermediate_schemas = intermediate_schemas

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
        # Resolve all intermediate schemas before processing any records.
        step_schemas: list[DatasetRecordSchema | None] = []
        expected_version = source_schema.version
        for step in path:
            if step.from_version != expected_version:
                raise SchemaEvolutionError(
                    f"migration path is discontinuous at {expected_version}"
                )
            expected_version = step.to_version
            if step.to_version == target_schema.version:
                step_schemas.append(target_schema)
            elif self._intermediate_schemas is not None:
                schema = self._intermediate_schemas.get_schema(
                    name=source_schema.name, version=step.to_version
                )
                if (
                    schema.name != source_schema.name
                    or schema.version != step.to_version
                ):
                    raise SchemaEvolutionError(
                        f"incorrect intermediate schema: {step.to_version}"
                    )
                step_schemas.append(schema)
            else:
                step_schemas.append(None)
        if expected_version != target_schema.version:
            raise SchemaEvolutionError("migration path must reach target version")

        migrated: list[dict[str, object]] = []
        for index, record in enumerate(records):
            try:
                self._validator.validate(
                    schema=source_schema, record=record
                )
                current = deepcopy(dict(record))
                for step, step_schema in zip(path, step_schemas, strict=True):
                    result = step.migrate(current)
                    if not isinstance(result, Mapping):
                        raise SchemaEvolutionError(
                            "migration must return a mapping"
                        )
                    current = deepcopy(dict(result))
                    if step_schema is not None:
                        self._validator.validate(
                            schema=step_schema, record=current
                        )
                self._validator.validate(
                    schema=target_schema, record=current
                )
                migrated.append(current)
            except SchemaEvolutionError as exc:
                raise SchemaEvolutionError(
                    f"record[{index}]: {exc}"
                ) from exc
        return tuple(migrated)
