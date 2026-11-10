"""Backward compatibility for strict versioned record schemas."""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import (
    DatasetRecordSchema,
    parse_schema_version,
)


@dataclass(frozen=True, slots=True)
class CompatibilityReport:
    source_version: str
    target_version: str
    breaking_changes: tuple[str, ...]
    safe_changes: tuple[str, ...]

    @property
    def backward_compatible(self) -> bool:
        """Whether old records pass the new schema's strict validator."""
        return not self.breaking_changes


class SchemaCompatibilityChecker:
    """Reports schema changes without performing data migrations."""

    def compare(
        self,
        *,
        source: DatasetRecordSchema,
        target: DatasetRecordSchema,
    ) -> CompatibilityReport:
        if source.name != target.name:
            raise SchemaEvolutionError("cannot compare different schema names")
        if parse_schema_version(target.version) < parse_schema_version(
            source.version
        ):
            raise SchemaEvolutionError("target schema version cannot decrease")
        if source.version == target.version and source != target:
            raise SchemaEvolutionError(
                "schema definition changed without a version bump"
            )

        old = {field.name: field for field in source.fields}
        new = {field.name: field for field in target.fields}
        breaking: list[str] = []
        safe: list[str] = []

        for name, before in old.items():
            after = new.get(name)
            if after is None:
                breaking.append(f"removed field: {name}")
                continue
            if before.kind != after.kind:
                breaking.append(f"changed type: {name}")
            if not before.required and after.required:
                breaking.append(f"required field tightened: {name}")
            elif before.required and not after.required:
                safe.append(f"required field relaxed: {name}")
            if before.nullable and not after.nullable:
                breaking.append(f"nullable field tightened: {name}")
            elif not before.nullable and after.nullable:
                safe.append(f"nullable field relaxed: {name}")

        for name, after in new.items():
            if name not in old:
                if after.required:
                    breaking.append(f"new required field: {name}")
                else:
                    safe.append(f"new optional field: {name}")

        return CompatibilityReport(
            source_version=source.version,
            target_version=target.version,
            breaking_changes=tuple(breaking),
            safe_changes=tuple(safe),
        )
