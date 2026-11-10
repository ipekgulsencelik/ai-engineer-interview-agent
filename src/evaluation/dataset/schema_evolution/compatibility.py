"""Strict-reader backward compatibility analysis for nested record schemas."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
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
        """Whether every old valid record passes the new strict validator."""
        return not self.breaking_changes


class SchemaCompatibilityChecker:
    """Classify reader compatibility, independent of migration availability."""

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
        breaking: list[str] = []
        safe: list[str] = []
        self._compare_fields(
            before={field.name: field for field in source.fields},
            after={field.name: field for field in target.fields},
            prefix="",
            breaking=breaking,
            safe=safe,
        )
        return CompatibilityReport(
            source_version=source.version,
            target_version=target.version,
            breaking_changes=tuple(breaking),
            safe_changes=tuple(safe),
        )

    def _compare_fields(
        self,
        *,
        before: Mapping[str, DatasetField],
        after: Mapping[str, DatasetField],
        prefix: str,
        breaking: list[str],
        safe: list[str],
    ) -> None:
        for name, old in before.items():
            path = f"{prefix}.{name}" if prefix else name
            new = after.get(name)
            if new is None:
                breaking.append(f"removed field: {path}")
            else:
                self._compare_field(
                    old=old, new=new, path=path, breaking=breaking, safe=safe
                )
        for name, new in after.items():
            if name not in before:
                path = f"{prefix}.{name}" if prefix else name
                destination = breaking if new.required else safe
                destination.append(
                    f"new {'required' if new.required else 'optional'} field: {path}"
                )

    def _compare_field(
        self,
        *,
        old: DatasetField,
        new: DatasetField,
        path: str,
        breaking: list[str],
        safe: list[str],
    ) -> None:
        if old.kind != new.kind:
            breaking.append(f"changed type: {path}")
            return
        if not old.required and new.required:
            breaking.append(f"required field tightened: {path}")
        elif old.required and not new.required:
            safe.append(f"required field relaxed: {path}")
        if old.nullable and not new.nullable:
            breaking.append(f"nullable field tightened: {path}")
        elif not old.nullable and new.nullable:
            safe.append(f"nullable field relaxed: {path}")

        if old.kind == "object":
            if not old.properties and new.properties:
                breaking.append(f"nested object constraints added: {path}")
            elif old.properties and not new.properties:
                safe.append(f"nested object constraints removed: {path}")
            elif old.properties and new.properties:
                self._compare_fields(
                    before={f.name: f for f in old.properties},
                    after={f.name: f for f in new.properties},
                    prefix=path,
                    breaking=breaking,
                    safe=safe,
                )
        if old.kind == "array":
            if old.items is None and new.items is not None:
                breaking.append(f"array item constraints added: {path}")
            elif old.items is not None and new.items is None:
                safe.append(f"array item constraints removed: {path}")
            elif old.items is not None and new.items is not None:
                self._compare_field(
                    old=old.items,
                    new=new.items,
                    path=f"{path}[]",
                    breaking=breaking,
                    safe=safe,
                )
