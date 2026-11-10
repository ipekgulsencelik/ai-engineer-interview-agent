"""Strict record validation with no implicit coercion."""

from __future__ import annotations

import math
from collections.abc import Mapping

from src.evaluation.dataset.schema_evolution.errors import SchemaEvolutionError
from src.evaluation.dataset.schema_evolution.models import (
    DatasetField,
    DatasetRecordSchema,
)


def _matches_kind(value: object, kind: str) -> bool:
    if kind == "string":
        return isinstance(value, str)
    if kind == "integer":
        return type(value) is int
    if kind == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    if kind == "boolean":
        return type(value) is bool
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    return False


class DatasetRecordValidator:
    """Validates records using an explicit, versioned dataset record schema."""

    def validate(
        self,
        *,
        schema: DatasetRecordSchema,
        record: Mapping[str, object],
    ) -> None:
        if not isinstance(record, Mapping):
            raise SchemaEvolutionError("record must be a mapping")
        field_map = {field.name: field for field in schema.fields}
        unknown = set(record) - set(field_map)
        if unknown:
            raise SchemaEvolutionError(
                f"unknown record fields: {sorted(unknown)}"
            )
        for field in schema.fields:
            self._validate_field(field=field, record=record)

    @staticmethod
    def _validate_field(
        *,
        field: DatasetField,
        record: Mapping[str, object],
    ) -> None:
        if field.name not in record:
            if field.required:
                raise SchemaEvolutionError(
                    f"missing required field: {field.name}"
                )
            return
        value = record[field.name]
        if value is None:
            if not field.nullable:
                raise SchemaEvolutionError(
                    f"field {field.name} cannot be null"
                )
        elif not _matches_kind(value, field.kind):
            raise SchemaEvolutionError(
                f"field {field.name} must have kind {field.kind}"
            )
