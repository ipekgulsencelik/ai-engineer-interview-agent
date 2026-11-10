"""Immutable schema contracts, versioned independently of dataset releases."""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError

FIELD_TYPES = frozenset(
    {"string", "integer", "number", "boolean", "object", "array"}
)
_SEMVER_PATTERN = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
)


def parse_schema_version(value: str) -> tuple[int, int, int]:
    """Return strict major/minor/patch components for a schema version."""
    if not isinstance(value, str):
        raise SchemaEvolutionError("schema version must be a string")
    match = _SEMVER_PATTERN.fullmatch(value)
    if match is None:
        raise SchemaEvolutionError(
            "schema version must use MAJOR.MINOR.PATCH"
        )
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


@dataclass(frozen=True, slots=True)
class DatasetField:
    name: str
    kind: str
    required: bool = True
    nullable: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise SchemaEvolutionError("field name must be non-empty")
        if not isinstance(self.kind, str) or self.kind not in FIELD_TYPES:
            raise SchemaEvolutionError(
                "unsupported field kind; use a JSON-compatible kind"
            )
        if type(self.required) is not bool or type(self.nullable) is not bool:
            raise SchemaEvolutionError("required and nullable must be booleans")


@dataclass(frozen=True, slots=True)
class DatasetRecordSchema:
    name: str
    version: str
    fields: tuple[DatasetField, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise SchemaEvolutionError("schema name must be non-empty")
        parse_schema_version(self.version)
        if not isinstance(self.fields, tuple) or not self.fields:
            raise SchemaEvolutionError("schema fields must be a non-empty tuple")
        if not all(isinstance(field, DatasetField) for field in self.fields):
            raise SchemaEvolutionError("all schema fields must be DatasetField")
        names = [field.name for field in self.fields]
        if len(names) != len(set(names)):
            raise SchemaEvolutionError("duplicate schema field name")
