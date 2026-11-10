"""Explicit, testable record migration operations and a linear registry."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from typing import Protocol

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import parse_schema_version


class MigrationOperation(Protocol):
    """One immutable-friendly transformation of an individual record."""

    def apply(self, record: Mapping[str, object]) -> Mapping[str, object]: ...


class RecordMigration(Protocol):
    @property
    def from_version(self) -> str: ...

    @property
    def to_version(self) -> str: ...

    def migrate(self, record: Mapping[str, object]) -> Mapping[str, object]: ...


class MigrationPathResolver(Protocol):
    def resolve(
        self, *, source_version: str, target_version: str
    ) -> tuple[RecordMigration, ...]: ...


@dataclass(frozen=True, slots=True)
class RenameField:
    source: str
    target: str

    def apply(self, record: Mapping[str, object]) -> dict[str, object]:
        result = dict(record)
        if self.source in result:
            if self.target in result:
                raise SchemaEvolutionError(
                    f"rename would overwrite existing field: {self.target}"
                )
            result[self.target] = result.pop(self.source)
        return result


@dataclass(frozen=True, slots=True)
class DropField:
    name: str

    def apply(self, record: Mapping[str, object]) -> dict[str, object]:
        result = dict(record)
        result.pop(self.name, None)
        return result


@dataclass(frozen=True, slots=True)
class SetDefault:
    name: str
    value: object

    def apply(self, record: Mapping[str, object]) -> dict[str, object]:
        result = dict(record)
        if self.name not in result:
            result[self.name] = deepcopy(self.value)
        return result


@dataclass(frozen=True, slots=True)
class MigrationStep:
    from_version: str
    to_version: str
    operations: tuple[MigrationOperation, ...]

    def __post_init__(self) -> None:
        if parse_schema_version(self.from_version) >= parse_schema_version(
            self.to_version
        ):
            raise SchemaEvolutionError(
                "migration destination must have a greater version"
            )
        if not isinstance(self.operations, tuple):
            raise SchemaEvolutionError("operations must be a tuple")

    def migrate(self, record: Mapping[str, object]) -> dict[str, object]:
        current = deepcopy(dict(record))
        for operation in self.operations:
            updated = operation.apply(current)
            if not isinstance(updated, Mapping):
                raise SchemaEvolutionError(
                    "migration operation must return a mapping"
                )
            current = deepcopy(dict(updated))
        return current


class MigrationRegistry:
    """Holds one directed migration path per version (no ambiguous forks)."""

    def __init__(self, migrations: Iterable[RecordMigration] = ()) -> None:
        self._by_source: dict[str, RecordMigration] = {}
        for migration in migrations:
            source = parse_schema_version(migration.from_version)
            target = parse_schema_version(migration.to_version)
            if target <= source:
                raise SchemaEvolutionError(
                    "migration destination must have a greater version"
                )
            if migration.from_version in self._by_source:
                raise SchemaEvolutionError(
                    f"duplicate migration from {migration.from_version}"
                )
            self._by_source[migration.from_version] = migration

    def resolve(
        self, *, source_version: str, target_version: str
    ) -> tuple[RecordMigration, ...]:
        current = parse_schema_version(source_version)
        target = parse_schema_version(target_version)
        if current > target:
            raise SchemaEvolutionError("schema downgrade is not supported")
        path: list[RecordMigration] = []
        version = source_version
        while current < target:
            step = self._by_source.get(version)
            if step is None:
                raise SchemaEvolutionError(
                    f"missing migration from {version} to {target_version}"
                )
            next_version = parse_schema_version(step.to_version)
            if next_version > target:
                raise SchemaEvolutionError(
                    "migration step overshoots target schema version"
                )
            path.append(step)
            current = next_version
            version = step.to_version
        return tuple(path)
